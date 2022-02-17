from random import random
from math import degrees, pi, sin, cos, atan2, sqrt, radians
from BasicElements import Transform, Pos, Rot
from copy import deepcopy


def generate(self, text, r) -> Transform:

    # random
    if text == 'random':
        last_theta_deg = self.lastTransform.rot.y
        while True:
            theta = random()*2*pi
            theta_deg = -degrees(theta) + 270
            if abs(theta_deg-last_theta_deg) >= 60:
                break
        while True:
            phi = random()/2*pi - pi / 6
            if r*sin(phi)+self.height >= 0:
                break
        pos = Pos(round(r*cos(phi)*cos(theta), 1),
                  round(r*sin(phi)+self.height, 1),
                  round(r*cos(phi)*sin(theta), 1)
                  )
        spin = random()*20-10
        rot = Rot(int(degrees(phi)),
                  -int(degrees(theta))+270,
                  spin)
        return Transform(pos, rot, self.fov)

    # center
    if text == 'center':
        if r >= 0:
            pos = Pos(0, self.height, r)
            rot = Rot(0, 180, 0)
        if r < 0:
            pos = Pos(0, self.height+abs(r), r)
            rot = Rot(40, 0, 0)
        return Transform(pos, rot, self.fov)

    # side
    if text == 'side':
        pos = Pos(r, self.height, 0)
        if r >= 0:
            rot = Rot(0, -90, 0)
        else:
            rot = Rot(0, 90, 0)
        return Transform(pos, rot, self.fov)

    # diagb
    if text == 'diagb':
        print(self.height)
        pos = Pos(r, 3.0, -abs(r))
        angle = degrees(atan2(self.height, abs(r)))
        print(angle)
        if r >= 0:
            rot = Rot(angle, -45, 0)
        else:
            rot = Rot(angle, 45, 0)
        return Transform(pos, rot, self.fov)

    # diagf
    if text == 'diagf':
        pos = Pos(r, 3.0, abs(r))
        angle = degrees(atan2(self.height, abs(r)))
        if r >= 0:
            rot = Rot(angle, -135, 0)
        else:
            rot = Rot(angle, 135, 0)
        return Transform(pos, rot, self.fov)

    # top
    if text == 'top':
        pos = Pos(0, r, r/10)
        rot = Rot(90, 0, 0)
        return Transform(pos, rot, self.fov)

    # dpos or q
    if text == 'dpos' or text == 'q':
        pos = Pos(0, 0, 0)
        rot = Rot(0, 0, 0)
        return Transform(pos, rot, self.fov)

    # stop
    if text == 'stop':
        return self.lastTransform

    # mirror
    if text == 'mirror':
        transform = deepcopy(self.lastTransform)
        transform.pos.x *= -1
        transform.rot.y *= -1
        return transform

    # zoom
    if text == 'zoom':
        transform = deepcopy(self.lastTransform)
        transform.fov -= r
        return transform

    # spin
    if text == 'spin':
        transform = deepcopy(self.lastTransform)
        transform.rot.z += r
        return transform

    # screw
    if text == 'screw':
        transform = deepcopy(self.lastTransform)
        transform.fov -= r
        transform.rot.z += r*2
        return transform

    # slide
    if text == 'slide':
        transform = deepcopy(self.lastTransform)
        transform.pos.x += r
        return transform

    # shift
    if text == 'shift':
        transform = deepcopy(self.lastTransform)
        transform.pos.y += r
        return transform

    # push
    if text == 'push':
        transform = deepcopy(self.lastTransform)
        transform.pos.z += r
        return transform

    # turn
    if text == 'turn':
        transform = deepcopy(self.lastTransform)
        px = transform.pos.x
        pz = transform.pos.z
        arm = sqrt(px**2+pz**2)
        theta = atan2(pz, px)
        theta += radians(r)
        transform.pos.x = arm * cos(theta)
        transform.pos.z = arm * sin(theta)
        transform.rot.y -= r
        return transform

    return self.lastTransform
