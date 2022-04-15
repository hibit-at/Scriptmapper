from random import random
from math import atan2, pi, sin, cos, degrees
from copy import deepcopy
from BasicElements import Pos, Rot, Line


def rotate(self, text, dur):
    # def_value
    r = 3
    h = 3
    a = 1
    o = 1.0
    s = 0
    j = 0
    w = 360
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
        if len(param) > 5:
            j = param[5]
        if len(param) > 6:
            w = param[6]
    self.logger.log(f'パラメータ r:{r} h:{h} a:{a} o:{o} s:{s} j:{j} w:{w}')
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
