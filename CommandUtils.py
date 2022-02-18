from BasicElements import Pos, Rot
from LongCommandsUtils import rotate, vibro
from PresetCommandsUtils import generate
from GeneralUtils import get_param


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
    if manu['fov'] == 'env':
        self.logger.log('オリジナルコマンドの fov が env になっているため、環境fovを引き継ぎます。')
        fov = self.fov
    else:
        fov = float(manu['fov'])
    transform.pos = pos
    transform.fov = fov
    print(manu)
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
    if pre_dollar[:4] == 'dpos' and pre_dollar[4] != '_':
        pre_dollar = 'dpos_' + pre_dollar[4:]
    if pre_dollar[:1] == 'q' and pre_dollar[1] != '_':
        pre_dollar = 'q_' + pre_dollar[1:]
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
