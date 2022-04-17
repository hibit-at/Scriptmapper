from random import random
from math import atan2, pi, sin, cos, tan, degrees, radians, sqrt
from copy import deepcopy
from BasicElements import Pos, Rot, Line


def rotate(self, text, dur):
    # def_value
    r1 = 3
    h1 = 3
    a = 1
    o = 1.0
    s1 = 0
    j = 0
    w = 360
    if len(text) > 6:
        param = [eval(i) for i in text[6:].split(',')]
        if len(param) > 0:
            r1 = param[0]
        if len(param) > 1:
            h1 = param[1]
        if len(param) > 2:
            a = param[2]
        if len(param) > 3:
            o = param[3]
        if len(param) > 4:
            s1 = param[4]
        if len(param) > 5:
            j = param[5]
        if len(param) > 6:
            w = param[6]
        if len(param) > 7:
            r2 = param[7]
        else:
            r2 = r1
        if len(param) > 8:
            h2 = param[8]
        else:
            h2 = h1
        if len(param) > 9:
            s2 = param[9]
        else:
            s2 = s1
    self.logger.log(f'パラメータ r1:{r1} h1:{h1} a:{a} o:{o} s1:{s1} j:{j} w:{w} r2:{r2} h2:{h2} s2:{s2}')
    span = max(1/30, dur/36)
    spans = []
    while dur > 0:
        min_span = min(span, dur)
        spans.append(min_span)
        dur -= min_span
    span_size = len(spans)
    for i in range(span_size):
        new_line = Line(spans[i])
        new_line.visibleDict = deepcopy(self.visibleObject.state)
        theta = 2*pi*i*(w/360)/span_size - 1/2*pi + j*2*pi/360
        next_theta = 2*pi*(i+1)*(w/360)/span_size - 1/2*pi + j*2*pi/360
        r = r1 + (r2-r1)*i/span_size
        h = h1 + (h2-h1)*i/span_size
        s = s1 + (s2-s1)*i/span_size
        angle = atan2(h-a, r)
        px = round(r*cos(theta), 3)
        pz = round(r*sin(theta)+o, 3)
        rx = degrees(angle)
        ry = -degrees(theta)+270
        new_line.start.pos = Pos(px, h, pz)
        new_line.start.rot = Rot(rx, ry, s)
        new_line.start.fov = self.fov
        r = r1 + (r2-r1)*(i+1)/span_size
        h = h1 + (h2-h1)*(i+1)/span_size
        s = s1 + (s2-s1)*(i+1)/span_size
        angle = atan2(h-a, r)
        px = round(r*cos(next_theta), 3)
        pz = round(r*sin(next_theta)+o, 3)
        rx = degrees(angle)
        ry = -degrees(next_theta)+270
        new_line.end.pos = Pos(px, h, pz)
        new_line.end.rot = Rot(rx, ry, s)
        new_line.end.fov = self.fov
        self.logger.log(new_line.start)
        self.lines.append(new_line)


def rot(self, dur, text, line):
    if len(param := text[3:].split('_')) == 3:
        n = eval(param[1])
        o = eval(param[2])
    else:
        self.logger.log(f'!（非公式機能）rotの後の数値が不正です !')
        self.logger.log(f'（非公式機能）rot: False としますが、意図しない演出になっています。')
        self.lines.append(line)
        self.logger.log(line.start)
        self.logger.log(line.end)
        return
    span = max(1/30, dur/36)
    spans = []
    while dur > 0:
        min_span = min(span, dur)
        spans.append(min_span)
        dur -= min_span
    span_size = len(spans)
    ixp, iyp, izp = line.start.pos.unpack()
    ixr, iyr, izr = line.start.rot.unpack()
    lxp, lyp, lzp = line.end.pos.unpack()
    lxr, lyr, lzr = line.end.rot.unpack()
    iFOV = line.start.fov
    lFOV = line.end.fov
    ir = sqrt(ixp**2+izp**2)
    lr = sqrt(lxp**2+lzp**2)
    itheta = atan2(izp, ixp)%(2*pi)
    ltheta = atan2(lzp, lxp)%(2*pi)
    if n > 0:
        dtheta = ltheta-itheta + 2*pi*(n-1)
    elif n < 0:
        dtheta = ltheta-itheta + 2*pi*n
    else:
        self.logger.log(f'!（非公式機能）rotのnパラメータが0です !')
        self.logger.log(f'（非公式機能）rot: False としますが、意図しない演出になっています。')
        self.lines.append(line)
        self.logger.log(line.start)
        self.logger.log(line.end)
        return
    self.logger.log(f'itheta: {itheta}, {atan2(izp, ixp)}')
    self.logger.log(f'ltheta: {ltheta}, {atan2(lzp, lxp)}')
    self.logger.log(f'dtheta: {dtheta}')
    for i in range(span_size):
        new_line = Line(spans[i])
        new_line.visibleDict = deepcopy(self.visibleObject.state)
        theta1 = itheta + dtheta*i/span_size
        r1 = ir + (lr-ir)*i/span_size
        h1 = iyp + (lyp-iyp)*i/span_size
        s1 = izr + (lzr-izr)*i/span_size
        fov1 = iFOV + (lFOV-iFOV)*i/span_size
        rx1 = ixr + (lxr-ixr)*i/span_size
        px = round(r1*cos(theta1), 3)
        pz = round(r1*sin(theta1)+o, 3)
        ry = -degrees(theta1)+270
        new_line.start.pos = Pos(px, h1, pz)
        new_line.start.rot = Rot(rx1, ry, s1)
        new_line.start.fov = fov1
        theta2 = itheta + dtheta*(i+1)/span_size
        r2 = ir + (lr-ir)*(i+1)/span_size
        h2 = iyp + (lyp-iyp)*(i+1)/span_size
        s2 = izr + (lzr-izr)*(i+1)/span_size
        fov2 = iFOV + (lFOV-iFOV)*(i+1)/span_size
        rx2 = ixr + (lxr-ixr)*(i+1)/span_size
        px = round(r2*cos(theta2), 3)
        pz = round(r2*sin(theta2)+o, 3)
        ry = -degrees(theta2)+270
        new_line.end.pos = Pos(px, h2, pz)
        new_line.end.rot = Rot(rx2, ry, s2)
        new_line.end.fov = fov2
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
        new_line.visibleDict = deepcopy(self.visibleObject.state)
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