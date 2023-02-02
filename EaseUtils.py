from copy import deepcopy
from math import cos, pi, sin, sqrt

from BasicElements import Pos, Rot, Line, Transform

# Reference: https://easings.net/

easetypes = ['InSine',
             'OutSine',
             'InOutSine',
             'InCubic',
             'OutCubic',
             'InOutCubic',
             'InQuint',
             'OutQuint',
             'InOutQuint',
             'InCirc',
             'OutCirc',
             'InOutCirc',
             'InElastic',
             'OutElastic',
             'InOutElastic',
             'InQuad',
             'OutQuad',
             'InOutQuad',
             'InQuart',
             'OutQuart',
             'InOutQuart',
             'InExpo',
             'OutExpo',
             'InOutExpo',
             'InBack',
             'OutBack',
             'InOutBack',
             'InBounce',
             'OutBounce',
             'InOutBounce',
             'Drift',
             ]


def InSine(t):
    return 1 - cos((t * pi) / 2)


def OutSine(t):
    return sin((t * pi) / 2)


def InOutSine(t):
    return -(cos(pi * t) - 1) / 2


def InCubic(t):
    return t * t * t


def OutCubic(t):
    return 1 - pow(1 - t, 3)


def InOutCubic(t):
    return 4 * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 3) / 2


def InQuint(t):
    return t * t * t * t * t


def OutQuint(t):
    return 1 - pow(1 - t, 5)


def InOutQuint(t):
    return 16 * t * t * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 5) / 2


def InCirc(t):
    return 1 - sqrt(1 - pow(t, 2))


def OutCirc(t):
    return sqrt(1 - pow(t - 1, 2))


def InOutCirc(t):
    return (1 - sqrt(1 - pow(2 * t, 2))) / 2 if t < 0.5 else (sqrt(1 - pow(-2 * t + 2, 2)) + 1) / 2


def InElastic(t):
    c4 = (2 * pi) / 3
    if t == 0:
        return 0
    elif t == 1:
        return 1
    else:
        return -pow(2, 10 * t - 10) * sin((t * 10 - 10.75) * c4)


def OutElastic(t):
    c4 = (2 * pi) / 3
    if t == 0:
        return 0
    elif t == 1:
        return 1
    else:
        return pow(2, -10 * t) * sin((t * 10 - 0.75) * c4) + 1


def InOutElastic(t):
    c5 = (2 * pi) / 4.5
    if t == 0:
        return 0
    elif t == 1:
        return 1
    elif t < 0.5:
        return -(pow(2, 20 * t - 10) * sin((20 * t - 11.125) * c5)) / 2
    else:
        return (pow(2, -20 * t + 10) * sin((20 * t - 11.125) * c5)) / 2 + 1


def InQuad(t):
    return t * t


def OutQuad(t):
    return 1 - (1 - t) * (1 - t)


def InOutQuad(t):
    return 2 * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 2) / 2


def InQuart(t):
    return t * t * t * t


def OutQuart(t):
    return 1 - pow(1 - t, 4)


def InOutQuart(t):
    return 8 * t * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 4) / 2


def InExpo(t):
    return 0 if t == 0 else pow(2, 10 * t - 10)


def OutExpo(t):
    return 1 if t == 1 else 1 - pow(2, -10 * t)


def InOutExpo(t):
    if t == 0:
        return 0
    elif t == 1:
        return 1
    elif t < 0.5:
        return pow(2, 20 * t - 10) / 2
    else:
        return (2 - pow(2, -20 * t + 10)) / 2


def InBack(t):
    c1 = 1.70158
    c3 = c1 + 1
    return c3 * t * t * t - c1 * t * t


def OutBack(t):
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2)


def InOutBack(t):
    c1 = 1.70158
    c2 = c1 * 1.525
    return (pow(2 * t, 2) * ((c2 + 1) * 2 * t - c2)) / 2 if t < 0.5 else (pow(2 * t - 2, 2) * ((c2 + 1) * (t * 2 - 2) + c2) + 2) / 2


def InBounce(t):
    return 1 - OutBounce(1 - t)


def OutBounce(t):
    n1 = 7.5625
    d1 = 2.75
    if t < (1 / d1):
        return n1 * t * t
    elif t < (2 / d1):
        return n1 * (t - 1.5 / d1)**2 + 0.75
    elif t < (2.5 / d1):
        return n1 * (t - 2.25 / d1)**2 + 0.9375
    else:
        return n1 * (t - 2.625 / d1)**2 + 0.984375


def InOutBounce(t):
    return (1 - OutBounce(1 - 2 * t)) / 2 if t < 0.5 else (1 + OutBounce(2 * t - 1)) / 2


def Drift(t, x=6, y=6):
    x /= 10
    y /= 10
    if x == 1 and y == 1:
        return t
    if x > y:
        hy = 0
        hx = (x-y)/(1-y)
    else:
        hx = 0
        hy = (y-x)/(1-x)
    if t >= x:
        return (1-t)/(1-x)*y + (t-x)/(1-x)
    else:
        ng = 0
        ok = 1
        while abs(ng-ok) > 1e-10:
            mid = ng + ok
            mid /= 2
            criteria = 3*(1-mid)*mid*mid*hx + mid*mid*mid*x
            if criteria >= t:
                ok = mid
            else:
                ng = mid
        return 3*(1-ok)*ok*ok*hy + ok*ok*ok*y


def interpolate(start, end, rate):
    return start*(1-rate) + end*rate


def ease(self, dur, text : str, line):
    u_text = text.upper()
    flag = 0
    dx = 6
    dy = 6
    if len(u_text.split('_')) > 2:
        dx = float(u_text.split('_')[1])
        dy = float(u_text.split('_')[2])
    print(dx, dy)
    if u_text != 'EASE':
        if u_text[:4] == 'EASE':
            u_text = u_text[4:]
        if u_text[:2] == 'IO':
            u_text = 'INOUT' + u_text[2:]
        if (u_text[0] == 'I') & (u_text[1] != 'N'):
            u_text = 'IN' + u_text[1:]
        if (u_text[0] == 'O') & (u_text[1] != 'U'):
            u_text = 'OUT' + u_text[1:]
        for easetype in easetypes:
            u_easetype = easetype.upper()
            if u_text.startswith(u_easetype):
                self.logger.log(f'easeコマンド {easetype} を検出')
                easefunc = eval(easetype)
                flag = 1
                break
    if flag == 0:
        if u_text.startswith('EASE'):
            self.logger.log(f'easeコマンドを検出')
            self.logger.log(
                f'有効なeasing関数名が指定されていないため、easeInOutCubic（CameraPlus デフォルト）を返します')
            easefunc = InOutCubic
        else:
            self.logger.log(f'! 有効なeaseコマンドを検出できません !')
            self.logger.log(f'EaseTransition: False としますが、意図しない演出になっています。')
            self.lines.append(line)
            self.logger.log(line.start)
            self.logger.log(line.end)
            return
    span = max(1/30, dur/36)
    spans = []
    init_dur = dur
    while dur > 0:
        min_span = min(span, dur)
        spans.append(min_span)
        dur -= min_span
    span_size = len(spans)
    ixp, iyp, izp = line.start.pos.unpack()
    ixr, iyr, izr = line.start.rot.unpack()
    lxp, lyp, lzp = line.end.pos.unpack()
    lxr, lyr, lzr = line.end.rot.unpack()
    lxr = ixr + (lxr - ixr + 180) % 360 - 180
    lyr = iyr + (lyr - iyr + 180) % 360 - 180
    lzr = izr + (lzr - izr + 180) % 360 - 180
    iFOV = line.start.fov
    lFOV = line.end.fov

    self.lastTransform = line.start
    for i in range(span_size):
        new_line = Line(spans[i])
        new_line.visibleDict = deepcopy(line.visibleDict)
        t = sum(spans[:(i+1)])/init_dur
        if easefunc != Drift:
            rate = easefunc(t)
        else:
            rate = Drift(t,dx,dy)
        new_line.start = deepcopy(self.lastTransform)
        endPos = Pos(
            interpolate(ixp, lxp, rate),
            interpolate(iyp, lyp, rate),
            interpolate(izp, lzp, rate),
        )
        endRot = Rot(
            interpolate(ixr, lxr, rate),
            interpolate(iyr, lyr, rate),
            interpolate(izr, lzr, rate),
        )
        fov = interpolate(iFOV, lFOV, rate)
        new_line.end = Transform(endPos, endRot, fov)
        self.logger.log(new_line.start)
        self.lines.append(new_line)
        self.lastTransform = new_line.end
