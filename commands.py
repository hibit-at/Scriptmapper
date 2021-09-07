from copy import deepcopy
from math import atan2, cos, degrees, pi, radians, sin, sqrt
from random import random as rd

from easefunc import *
from utils import create_template

command_values = {
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
}

# 座標新規生成系


def random(r, last_pos_rot, fov, height):
    last_theta_deg = last_pos_rot[1]['y']
    while True:
        theta = rd()*2*pi
        theta_deg = -degrees(theta) + 270
        if abs(theta_deg-last_theta_deg) >= 60:
            break
    while True:
        phi = rd()/2*pi - pi / 6
        if r*sin(phi)+height >= 0:
            break
    pos = {'x': round(r*cos(phi)*cos(theta), 1),
           'y': round(r*sin(phi)+height, 1),
           'z': round(r*cos(phi)*sin(theta), 1),
           'FOV': fov}
    spin = rd()*20-10
    rot = {'x': int(degrees(phi)),
           'y': -int(degrees(theta))+270,
           'z': spin}
    return pos, rot


def center(r, last_post_rot, fov, height):
    if r >= 0:
        pos = {'x': 0,
               'y': height,
               'z': r}
        rot = {'x': 0,
               'y': 180,
               'z': 0}
    if r < 0:
        pos = {'x': 0,
               'y': height+abs(r),
               'z': r}
        rot = {'x': 40,
               'y': 0,
               'z': 0}
    pos['FOV'] = fov
    return pos, rot


def side(r, last_pos_rot, fov, height):
    pos = {'x': r,
           'y': height,
           'z': 0,
           'FOV': fov}
    if r >= 0:
        rot = {'x': 0,
               'y': -90,
               'z': 0}
    else:
        rot = {'x': 0,
               'y': 90,
               'z': 0}
    return pos, rot


def top(h, last_pos_rot, fov, height):
    pos = {'x': 0,
           'y': h,
           'z': h/10,
           'FOV': fov}
    rot = {'x': 90,
           'y': 0,
           'z': 0}
    return pos, rot


def diagb(r, last_pos_rot, fov, height):
    pos = {'x': r,
           'y': 3.0,
           'z': -abs(r),
           'FOV': fov}
    angle = degrees(atan2(height, abs(r)))
    if r >= 0:
        rot = {'x': angle,
               'y': -45,
               'z': 0}
    if r < 0:
        rot = {'x': angle,
               'y': 45,
               'z': 0}
    return pos, rot


def diagf(r, last_pos_rot, fov, height):
    pos = {'x': r,
           'y': 3.0,
           'z': abs(r),
           'FOV': fov}
    angle = degrees(atan2(height, abs(r)))
    if r >= 0:
        rot = {'x': angle,
               'y': -135,
               'z': 0}
    if r < 0:
        rot = {'x': angle,
               'y': 135,
               'z': 0}
    return pos, rot


# 座標変化系

def mirror(dummy, last_pos_rot, fov, height):
    pos, rot = deepcopy(last_pos_rot)
    pos['x'] *= -1
    rot['y'] *= -1
    return pos, rot


def zoom(r, last_pos_rot, fov, height):
    pos, rot = deepcopy(last_pos_rot)
    pos['FOV'] -= r
    return pos, rot


def spin(r, last_pos_rot, fov, height):
    pos, rot = deepcopy(last_pos_rot)
    rot['z'] += r
    return pos, rot


def screw(r, last_pos_rot, fov, height):
    pos, rot = deepcopy(last_pos_rot)
    pos['FOV'] -= r
    rot['z'] += r*2
    return pos, rot


def slide(r, last_pos_rot, fov, height):
    pos, rot = deepcopy(last_pos_rot)
    pos['x'] += r
    return pos, rot


def shift(r, last_pos_rot, fov, height):
    pos, rot = deepcopy(last_pos_rot)
    pos['y'] += r
    return pos, rot


def push(r, last_pos_rot, fov, height):
    pos, rot = deepcopy(last_pos_rot)
    pos['z'] += r
    return pos, rot


def turn(r, last_pos_rot, fov, height):
    pos, rot = deepcopy(last_pos_rot)
    px = pos['x']
    pz = pos['z']
    arm = sqrt(px**2+pz**2)
    theta = atan2(pz, px)
    theta += radians(r)
    pos['x'] = arm * cos(theta)
    pos['z'] = arm * sin(theta)
    rot['y'] -= r
    return pos, rot


def stop(dummy, last_pos_rot, fov, height):
    pos, rot = deepcopy(last_pos_rot)
    return pos, rot


# オリジナルコマンド

def original(command, height):
    cx = float(command['px'])
    cy = float(command['py'])
    cz = float(command['pz'])
    fov = int(command['fov'])
    pos = {'x': cx, 'y': cy, 'z': cz, 'FOV': fov}
    if command['lookat'].lower() == 'true':
        theta = atan2(cz, cx)
        theta = -int(degrees(theta))+270
        r = sqrt(cx**2+cz**2)
        angle = int(degrees(atan2(cy-height, r)))
        rot = {'x': angle, 'y': theta, 'z': 0}
    else:
        rot = {'x': float(command['rx']), 'y': float(
            command['ry']), 'z': float(command['rz'])}
    return pos, rot

# 区間コマンド


def rotate(dur, text):
    log_text = ''
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
    log_text += f'パラメータ r:{r} h:{h} a:{a} o:{o} s:{s}\n'
    span = max(1/30, dur/36)
    spans = []
    while dur > 0.001:
        min_span = min(span, dur)
        spans.append(min_span)
        dur -= min_span
    span_size = len(spans)
    ans = []
    for i in range(span_size):
        new_line = create_template()
        theta = 2*pi*i/span_size - 1/2*pi
        next_theta = 2*pi*(i+1)/span_size - 1/2*pi
        angle = atan2(h-a, r)
        px = round(r*cos(theta), 3)
        pz = round(r*sin(theta)+o, 3)
        rx = degrees(angle)
        ry = -degrees(theta)+270
        new_line['StartPos'] = {'x': px, 'y': h, 'z': pz}
        new_line['StartRot'] = {'x': rx, 'y': ry, 'z': s}
        px = round(r*cos(next_theta), 3)
        pz = round(r*sin(next_theta)+o, 3)
        rx = degrees(angle)
        ry = -degrees(next_theta)+270
        new_line['EndPos'] = {'x': px, 'y': h, 'z': pz}
        new_line['EndRot'] = {'x': rx, 'y': ry, 'z': s}
        new_line['Duration'] = spans[i]
        log_text += f'start POS{new_line["StartPos"]} ROT{new_line["StartRot"]}\n'
        log_text += f'end POS{new_line["EndPos"]} ROT{new_line["EndRot"]}\n'
        ans.append(new_line)
    return ans, log_text


def vibro(dur, bpm, param, last_pos_rot):
    log_text = ''
    steps = []
    pos, rot = deepcopy(last_pos_rot)
    span = max(1/30, param*60/bpm)
    while dur > 0:
        steps.append(min(span, dur))
        dur -= span
        span *= (0.9 + rd()*0.2)
    ans = []
    for s in steps:
        new_line = create_template()
        new_line['StartPos'] = pos
        new_line['StartRot'] = rot
        e_pos, e_rot = deepcopy((pos, rot))
        dx = round(rd()/6, 3)-1/12
        dy = round(rd()/6, 3)-1/12
        dz = round(rd()/6, 3)-1/12
        e_pos['x'] += dx
        e_pos['y'] += dy
        e_pos['z'] += dz
        new_line['EndPos'] = e_pos
        new_line['EndRot'] = e_rot
        new_line['Duration'] = s
        ans.append(new_line)
        pos, rot = (e_pos, e_rot)
        log_text += f'start POS{new_line["StartPos"]} ROT{new_line["StartRot"]}\n'
        log_text += f'end POS{new_line["EndPos"]} ROT{new_line["EndRot"]}\n'
    return ans, log_text


def ease(dur, text, line, isHead, height):  # レイクンさんへ。追従モードのON/OFFと、アバターの身長設定を追加しました。
    log_text = ''
    u_text = text.upper()
    flag = 0
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
                log_text += f'easeコマンド {easetype} を検出'
                easefunc = eval(easetype)
                flag = 1
                break
    if flag == 0:
        if u_text.startswith('EASE'):
            log_text += f'easeコマンドを検出\n'
            log_text += f'有効なeasing関数名が指定されていないため、easeInOutCubic(CameraPlusデフォルト)を返します'
            easefunc = InOutCubic
        else:
            log_text += f'！有効なeaseコマンドを検出できません！\n'
            log_text += f'EaseTransition: False としますが、意図しない演出になっています。'
            return [line], log_text
    span = max(1/30, dur/36)
    spans = []
    init_dur = deepcopy(dur)
    while dur > 0.001:
        min_span = min(span, dur)
        spans.append(min_span)
        dur -= min_span
    span_size = len(spans)
    ixp, iyp, izp = line['StartPos']['x'], line['StartPos']['y'], line['StartPos']['z']
    ixr, iyr, izr = line['StartRot']['x'], line['StartRot']['y'], line['StartRot']['z']
    lxp, lyp, lzp = line['EndPos']['x'], line['EndPos']['y'], line['EndPos']['z']
    lxr, lyr, lzr = line['EndRot']['x'], line['EndRot']['y'], line['EndRot']['z']
    # fovの設定も追加しています。
    iFOV = line['StartPos']['FOV']
    lFOV = line['EndPos']['FOV']
    #
    dxp, dyp, dzp = (lxp - ixp), (lyp - iyp), (lzp - izp)
    dxr, dyr, dzr = (lxr % 360 - ixr % 360), (lyr %
                                              360 - iyr % 360), (lzr % 360 - izr % 360)
    # dr の補正、前のプログラムだと abs(lr-ir)>180 の状況だと補正が効かなかったので修正しました。
    dxr = (dxr+180) % 360 - 180
    dyr = (dyr+180) % 360 - 180
    dzr = (dzr+180) % 360 - 180
    # fov
    dFOV = lFOV-iFOV
    #
    lastpos = {'x': ixp, 'y': iyp, 'z': izp, 'FOV': iFOV}
    lastrot = {'x': ixr, 'y': iyr, 'z': izr}
    ans = []
    for i in range(span_size):
        new_line = create_template(isHead, height)
        t = sum(spans[:(i+1)])/init_dur
        rate = easefunc(t)
        new_line['StartPos'] = lastpos.copy()
        new_line['StartRot'] = lastrot.copy()
        new_line['EndPos'] = {'x': ixp+dxp*rate,
                              'y': iyp+dyp*rate, 'z': izp+dzp*rate,
                              'FOV': iFOV + dFOV*rate}
        new_line['EndRot'] = {'x': ixr+dxr*rate,
                              'y': iyr+dyr*rate, 'z': izr+dzr*rate}
        new_line['Duration'] = spans[i]
        # easeの場合はspan毎に逐一ログ出すのは煩雑すぎ？
        # log_text += f'start POS{new_line["StartPos"]} ROT{new_line["StartRot"]}\n'
        # log_text += f'end POS{new_line["EndPos"]} ROT{new_line["EndRot"]}\n'
        ans.append(new_line)
        lastpos = new_line['EndPos'].copy()
        lastrot = new_line['EndRot'].copy()
    return ans, log_text
