from random import random
from math import degrees, pi, sin, cos, atan2, sqrt
from BasicElements import Transform, Pos, Rot, Line
from copy import deepcopy

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


def rotate(self, text, dur):
    # def_value
    r = 3
    h = 3
    a = 1
    o = 1.0
    s = 0
    if len(text) > 6:
        param = [eval(i) for i in text[6:].split(',')]
        if len(param) > 0:
            r = param[0]
        if len(param) > 1:
            h = param[1]
        if len(param) > 2:
            a = param[2]
        if len(param) > 3:
            o = param[3]
        if len(param) > 4:
            s = param[4]
    self.logger.log(f'パラメータ r:{r} h:{h} a:{a} o:{o} s:{s}\n')
    span = max(1/30, dur/36)
    spans = []
    while dur > 0:
        min_span = min(span, dur)
        spans.append(min_span)
        dur -= min_span
    span_size = len(spans)
    for i in range(span_size):
        new_line = Line(spans[i])
        theta = 2*pi*i/span_size - 1/2*pi
        next_theta = 2*pi*(i+1)/span_size - 1/2*pi
        angle = atan2(h-a, r)
        px = round(r*cos(theta), 3)
        pz = round(r*sin(theta)+o, 3)
        rx = degrees(angle)
        ry = -degrees(theta)+270
        new_line.start.pos = Pos(px, h, pz)
        new_line.start.rot = Rot(rx, ry, s)
        new_line.start.fov = self.fov
        px = round(r*cos(next_theta), 3)
        pz = round(r*sin(next_theta)+o, 3)
        rx = degrees(angle)
        ry = -degrees(next_theta)+270
        new_line.end.pos = Pos(px, h, pz)
        new_line.end.rot = Rot(rx, ry, s)
        new_line.end.fov = self.fov
        self.logger.log(new_line.start)
        self.lines.append(new_line)


def vibro(self, dur, param):
    steps = []
    bpm = self.bpm
    span = max(1/30, param*60/bpm)
    while dur > 0:
        steps.append(min(span, dur))
        dur -= span
        span *= (0.9 + random()*0.2)
    ans = []
    for step in steps:
        new_line = Line(step)
        new_line.start = deepcopy(self.lastTransform)
        new_line.end = deepcopy(self.lastTransform)
        dx = round(random()/6, 3)-1/12
        dy = round(random()/6, 3)-1/12
        dz = round(random()/6, 3)-1/12
        new_line.end.pos.x += dx
        new_line.end.pos.y += dy
        new_line.end.pos.z += dz
        self.lastTransform = new_line.end
        ans.append(new_line)
        self.logger.log(new_line.start)
        self.lines.append(new_line)


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
    transform.set(generate(self, 'center', -2))


def env_command(self, text) -> None:
    if text[:3] == 'fov':
        param = get_param(self, text, 3, 60)
        self.logger.log('fov コマンドを検出。FOVを以下の値にします。 : ', param)
        self.fov = param
    elif text[:4] == 'seed':
        param = get_param(self, text, 4, 0)
        self.logger.log('seed コマンドを検出。ランダムシードを以下の値にします。 : ', param)
        self.seed(param)
        self.lastTransform = generate(self, 'center', -2)
    elif text[:4] == 'head':
        self.logger.log('head コマンドを検出。HMD追従モードを切り替えます。',
                        self.turnToHead, '->', not self.turnToHead)
        self.turnToHead = not self.turnToHead
    elif text[:7] == 'horizo':
        self.logger.log('horizo コマンドを検出。HMD追従モードを切り替えます。',
                        self.turnToHeadHorizontal, '->', not self.turnToHeadHorizontal)
        self.turnToHeadHorizontal = not self.turnToHeadHorizontal
    elif text[:6] == 'height':
        param = get_param(self, text, 6, 1.5)
        self.logger.log('height コマンドを検出。アバターの視点を以下の値にします。 : ', param)
        self.height = param
    else:
        self.logger.log('! 有効な環境コマンドを検出できません !')
