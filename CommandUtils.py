from BasicElements import Pos, Rot
from LongCommands import rotate, vibro
from PresetCommands import generate


commands = {
    'random': 4,
    'center': -2,
    'side': 2.5,
    'diagf': 4,
    'diagb': 4,
    'top': 3,
    'mirror': '-',
    'zoom': 2,
    'spin': 20,
    'screw': 2,
    'slide': 1,
    'shift': .5,
    'push': 1,
    'turn': 30,
    'stop': '-',
    'dpos': '-',
    'q': '-',
}


def get_param(self, text, length, def_value) -> float:
    param = def_value
    if len(text) > length:
        param_word = text[length:]
        check = any([c.isalpha() for c in param_word])
        if check:
            self.logger.log(f'パラメータ {param_word} に英字を確認。' +
                            f'セキュリティの問題上、プログラムを強制終了します。')
            input()
            exit()
        param = eval(param_word)
    return param


def adjust(self, transform, dollar_split) -> None:
    if len(dollar_split) > 1:
        adjust_command = dollar_split[1:]
        for a in adjust_command:
            self.logger.log(f'調整コマンド {a} を確認')
            inital = a[0]
            param = float(a[1:])
            if inital == 'X':
                transform.pos.x = param
            elif inital == 'Y':
                transform.pos.y = param
            elif inital == 'Z':
                transform.pos.z = param
            elif inital == 'F':
                transform.fov = param
            elif inital == 'x':
                transform.rot.x = param
            elif inital == 'y':
                transform.rot.y = param
            elif inital == 'z':
                transform.rot.z = param
            else:
                self.logger.log('無効な調整コマンドです。調整は行われません。')


def sequential(self, transform, text, under_split) -> None:
    if len(under_split) > 1:
        after_under = under_split[1:]
        if text[:4] == 'dpos':
            for i, a in enumerate(after_under):
                param = float(a)
                self.logger.log(f'dpos シーケンシャル調整_{param}')
                if i == 0:
                    transform.pos.x = param
                if i == 1:
                    transform.pos.y = param
                if i == 2:
                    transform.pos.z = param
                if i == 3:
                    transform.fov = param
            transform.lookat(self.height, self.lastTransform)
        elif text[0] == 'q':
            for i, a in enumerate(after_under):
                param = float(a)
                self.logger.log(f'q シーケンシャル調整_{param}')
                if i == 0:
                    transform.pos.x = param
                if i == 1:
                    transform.pos.y = param
                if i == 2:
                    transform.pos.z = param
                if i == 3:
                    transform.rot.x = param
                if i == 4:
                    transform.rot.y = param
                if i == 5:
                    transform.rot.z = param
                if i == 6:
                    transform.fov = param
        else:
            self.logger.log('このコマンドはシーケンシャル調整に対応していません')


def orig_command(self, key, transform):
    manu = self.manual[key]
    print(manu)
    pos = Pos(float(manu['px']), float(manu['py']), float(manu['pz']))
    if manu['fov'].lower() == 'env':
        self.logger.log('オリジナルコマンドの fov が env になっているため、環境fovを引き継ぎます。')
        fov = self.fov
    else:
        fov = float(manu['fov'])
    transform.pos = pos
    transform.fov = fov
    if manu['lookat'].lower() == 'true':
        self.logger.log('オリジナルコマンドの lookat が true になっているため、角度を自動計算します')
        transform.lookat(self.height, self.lastTransform)
    else:
        rot = Rot(float(manu['rx']), float(manu['ry']), float(manu['rz']))
        transform.rot = rot


def long_command(self, text, dur) -> bool:
    # rotate
    if text[:6] == 'rotate':
        self.logger.log(text)
        self.logger.log('rotate コマンドを確認')
        if any([c.isalpha() for c in text[6:]]):
            self.logger.log(
                f'パラメータ {text[6:]} に英字を確認。セキュリティの問題上、プログラムを強制終了します。')
            input()
            exit()
        rotate(self, text, dur)
        return True
    # vibro
    if text[:5] == 'vibro':
        self.logger.log(text)
        param = get_param(self, text, 5, def_value=1/4)
        self.logger.log('vibro コマンドを確認 ', param)
        vibro(self, dur, param)
        return True
    return False


def parse_command(self, transform, text) -> None:
    # dollar_check
    dollar_split = text.split('$')
    pre_dollar = dollar_split[0]
    # split_check
    under_split = pre_dollar.split('_')
    text = under_split[0]
    for key in self.manual.keys():
        if text == key:
            self.logger.log(f'オリジナルコマンド {key} を検出')
            # command = self.manual[key]
            orig_command(self, key, transform)
            return
    for c in commands:
        if text.startswith(c):
            leng = len(c)
            param = get_param(self, text, leng, commands[c])
            self.logger.log(f'{c} コマンドを検出  パラメータ : ', param)
            transform.set(generate(self, c, param))
            sequential(self, transform, text, under_split)
            adjust(self, transform, dollar_split)
            return
    self.logger.log(f'! スクリプト {text} はコマンドに変換できません !')
    self.logger.log('直前の座標を返しますが、意図しない演出になっています。')
    transform.set(self.lastTransform)


def env_command(self, text) -> None:
    if text[:3] == 'fov':
        param = get_param(self, text, 3, 60)
        self.logger.log('fov コマンドを検出。FOVを以下の値にします。 : ', param)
        self.fov = param
        return
    if text[:4] == 'seed':
        param = get_param(self, text, 4, 0)
        self.logger.log('seed コマンドを検出。ランダムシードを以下の値にします。 : ', param)
        self.seed(param)
        self.lastTransform = generate(self, 'center', -2)
        return
    if text[:4] == 'head':
        self.logger.log('head コマンドを検出。HMD追従モードを切り替えます。',
                        self.turnToHead, '->', not self.turnToHead)
        self.turnToHead = not self.turnToHead
        return
    if text[:7] == 'horizo':
        self.logger.log('horizo コマンドを検出。HMD追従モードを切り替えます。',
                        self.turnToHeadHorizontal, '->', not self.turnToHeadHorizontal)
        self.turnToHeadHorizontal = not self.turnToHeadHorizontal
        return
    if text[:6] == 'height':
        param = get_param(self, text, 6, 1.5)
        self.logger.log('height コマンドを検出。アバターの視点を以下の値にします。 : ', param)
        self.height = param
        return
    visibleObjects = ['avatar', 'ui', 'wall',
                      'wallFrame', 'saber', 'notes', 'debris']
    for visibleObject in visibleObjects:
        leng = len(visibleObject)
        if text[:leng] == visibleObject:
            self.logger.log(f'{visibleObject} コマンドを検出。')
            param = text[leng:]
            if param.upper() == 'ON':
                self.visible.append({'target': visibleObject, 'state': True})
                self.logger.log(
                    f'パラメータは ON です。次のコマンドで、{visibleObject} を ON にします。')
            elif param.upper() == 'OFF':
                self.visible.append({'target': visibleObject, 'state': False})
                self.logger.log(
                    f'パラメータは OFF です。次のコマンドで、{visibleObject} を OFF にします。')
            else:
                self.logger.log('パラメータを検出できません。')
            return
    self.logger.log('! 有効な環境コマンドを検出できません !')
