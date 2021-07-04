import json
import csv
import copy
import os
import pathlib
import sys
from random import random as rd
from math import sqrt, degrees, atan2, pi, floor, cos, sin
from datetime import date, datetime

# ログファイルの作成

now = str(datetime.now()).replace(':', '_')[:19]

with open(f'log_{now}.txt', 'w', encoding='utf-8') as f:
    f.write(f"logfile at {now}\n\n")


def print_log(*args):
    for a in args:
        print(a)
        with open(f'log_{now}.txt', 'a', encoding='utf-8') as f:
            f.write(str(a)+'\n')

# 関数の定義


template = {
    "ActiveInPauseMenu": True,
    "Movements": [
        {
            "StartPos": {
                "x": 0,
                "y": 0,
                "z": 0
            },
            "StartRot": {
                "x": 0,
                "y": 0,
                "z": 0
            },
            "EndPos": {
                "x": 0,
                "y": 0,
                "z": 0
            },
            "EndRot": {
                "x": 0,
                "y": 0,
                "z": 0
            },
            "Duration": 0,
            "Delay": 0,
            "EaseTransition": False
        }
    ]
}


def random(r):
    theta = rd()*2*pi
    phi = rd()/3*pi+pi/18
    angle = atan2(r*sin(phi)-1.0, r)
    pos = {'x': round(r*cos(phi)*cos(theta), 1),
           'y': round(r*sin(phi), 1),
           'z': round(r*cos(phi)*sin(theta), 1)}
    spin = rd()*20-10
    rot = {'x': int(degrees(angle)),
           'y': -int(degrees(theta))+270,
           'z': spin}
    return pos, rot


def front(r):
    pos = {'x': 0,
           'y': 1.5,
           'z': r}
    rot = {'x': 0,
           'y': 180,
           'z': 0}
    return pos, rot


def default():
    pos = {'x': 0,
           'y': 2,
           'z': -3}
    rot = {'x': 10,
           'y': 0,
           'z': 0}
    return pos, rot


def create_template():
    move_tmp = copy.deepcopy(template['Movements'][0])
    move_tmp['EaseTransition'] = False
    return move_tmp


def generate(text):
    global last_pos_rot
    if text[:6] == 'random':
        param = float(text[6:])
        print_log('random コマンドを検出', param)
        return random(param)
    elif text[:5] == 'front':
        param = float(text[5:])
        print_log('front コマンドを検出', param)
        return front(param)
    elif text[:6] == "mirror":
        print_log('mirror コマンドを検出')
        mirror_pos_rot = copy.deepcopy(last_pos_rot)
        mirror_pos_rot[0]['x'] *= -1
        mirror_pos_rot[1]['y'] *= -1
        return mirror_pos_rot
    elif text[:4] == "zoom":
        if len(text) == 4:
            param = 2
        else:
            param = float(text[4:])
        print_log('zoom コマンドを検出', param)
        zoom_pos_rot = copy.deepcopy(last_pos_rot)
        zoom_pos_rot[0]['x'] /= param
        zoom_pos_rot[0]['y'] -= 1.0
        zoom_pos_rot[0]['y'] /= param
        zoom_pos_rot[0]['y'] += 1.0
        zoom_pos_rot[0]['z'] /= param
        return zoom_pos_rot
    elif text[:4] == 'spin':
        print_log('spin コマンドを検出')
        param = float(text[4:])
        spin_pos_rot = copy.deepcopy(last_pos_rot)
        spin_pos_rot[1]['z'] += param
        return spin_pos_rot
    elif text[:5] == 'slide':
        param = float(text[5:])
        print_log('slide コマンドを検出', param)
        slide_pos_rot = copy.deepcopy(last_pos_rot)
        slide_pos_rot[0]['x'] += param
        return slide_pos_rot
    elif text[:5] == 'shift':
        param = float(text[5:])
        print_log('shift コマンドを検出', param)
        shift_pos_rot = copy.deepcopy(last_pos_rot)
        shift_pos_rot[0]['y'] += param
        return shift_pos_rot
    elif text[:6] == 'before':
        print_log('before コマンドを検出')
        new_pos_rot = copy.deepcopy(last_pos_rot)
        return new_pos_rot
    elif text[:3] == 'def':
        print_log('default コマンドを検出')
        return default()
    else:
        if text in manual.keys():
            print_log(f'オリジナルコマンド {text} を検出')
            command = manual[text]
            cx = float(command['px'])
            cy = float(command['py'])
            cz = float(command['pz'])
            pos = {'x': cx, 'y': cy, 'z': cz}
            if command['lookat'].lower() == 'true':
                theta = atan2(cz, cx)
                theta = -int(degrees(theta))+270
                r = sqrt(cx**2+cz**2)
                angle = int(degrees(atan2(cy-1.0, r)))
                rot = {'x': angle, 'y': theta, 'z': 0}
            else:
                rot = {'x': float(command['rx']), 'y': float(
                    command['ry']), 'z': float(command['rz'])}
            return pos, rot
        else:
            print_log('コマンドに該当なし、直近の値を返します。')
            return last_pos_rot

# 関数の定義　終わり


# 引数の取得
file_path = sys.argv[1]

path_obj = pathlib.Path(file_path)
path_dir = path_obj.parent

isWIP = path_obj.parent.parent

if not isWIP.name == 'CustomWIPLevels':
    print_log('WIPフォルダ直下にありません。プログラムを終了します。')
    wait = input()
    exit()

print_log('WIPフォルダ直下にあることを確認\n')

info_path = os.path.join(path_dir, 'info.dat')

if not os.path.exists(info_path):
    print_log('info.dat が見つかりません。プログラムを終了します。')
    exit()

f = open('info.dat', 'rb')
j = json.load(f)

bpm = j['_beatsPerMinute']
print_log('bpmを計測', bpm, '')

if os.path.exists('input.csv'):

    print_log('input.csv を確認しました。オリジナルコマンドを追加します。')
    data = csv.DictReader(open('input.csv', 'r', encoding='utf-8-sig'))
    manual = {}

    for d in data:
        manual[d['label']] = d
        print_log(d)

print_log('')

f = open(file_path, 'r')
j = json.load(f)

notes = j['_notes']

last_time = notes[-1]['_time']

if '_customData' in j.keys():
    raw_b = j['_customData']['_bookmarks']
else:
    raw_b = j['_bookmarks']

size = len(raw_b)

# time = 0 がない場合はstartを追加する
# 最後のノーツに達してない場合はそれをendとする

print_log('スクリプトの整形を開始')

filled_b = []
for i in range(size):
    time = raw_b[i]['_time']
    text = raw_b[i]['_name']
    if i == 0 and time != 0:
        filled_b.append({'time': 0, 'text': 'def'})
    filled_b.append({'time': time, 'text': text})

if filled_b[-1]['time'] < last_time:
    filled_b.append({'time': last_time, 'text': 'end'})

size = len(filled_b)
timed_b = []


for i in range(size-1):
    dur = filled_b[i+1]['time'] - filled_b[i]['time']
    text = filled_b[i]['text']
    if text[:4] == 'fill':
        param = int(text.split(',')[0][4:])
        print_log('特殊コマンド fill を検出', param)
        text_pattern = ','.join(text.split(',')[1:])
        span = 1/param
        print_log(
            f'スクリプト {text_pattern} をグリッド {filled_b[i]["time"]} から {filled_b[i+1]["time"]} まで{span}の間隔で敷き詰めます。')
        cnt = 0
        current_grid = filled_b[i]['time']
        while dur > 0.0001:
            cnt += 1
            timed_b.append({'dur': span*60/bpm, 'text': text_pattern})
            print_log(f'{text_pattern} {current_grid}')
            current_grid += span
            dur -= span
        print_log(f'n = {cnt}')
    else:
        timed_b.append({'dur': dur*60/bpm, 'text': text})


print_log('\nスクリプトの整形を完了。')
# これが最終的なスクリプト群に

data = copy.deepcopy(template)
data['Movements'] = []

last_pos_rot = ()

cnt = 0

for b in timed_b:
    cnt += 1
    print_log(f'\n{cnt}番目のスクリプト原文を確認中...')
    text = b['text']
    parse = text.split(',')
    if len(parse) == 1:
        print_log(f'1つのスクリプト {parse[0]} を確認。startとendに同じ値を設定します。')
        command = parse[0]
        # rotate
        if command[:6] == 'rotate':
            param = [float(i) for i in command[6:].split('/')]
            print_log('rotate コマンドを確認', param)
            r = param[0]
            h = param[1]
            dur = b['dur']
            span = max(1/30, dur/36)
            spans = []
            while dur > 0.001:
                min_span = min(span, dur)
                spans.append(min_span)
                dur -= min_span
            span_size = len(spans)
            print(span, span_size)
            for i in range(span_size):
                new_line = create_template()
                theta = 2*pi*i/span_size - 1/2*pi
                next_theta = 2*pi*(i+1)/span_size - 1/2*pi
                angle = atan2(h-1, r)
                px = round(r*cos(theta), 3)
                pz = round(r*sin(theta)+1, 3)
                rx = degrees(angle)
                ry = -degrees(theta)+270
                print_log({'x': px, 'y': h, 'z': pz},
                          {'x': rx, 'y': ry, 'z': 0})
                new_line['StartPos'] = {'x': px, 'y': h, 'z': pz}
                new_line['StartRot'] = {'x': rx, 'y': ry, 'z': 0}
                px = round(r*cos(next_theta), 3)
                pz = round(r*sin(next_theta)+1, 3)
                rx = degrees(angle)
                ry = -degrees(next_theta)+270
                new_line['EndPos'] = {'x': px, 'y': h, 'z': pz}
                new_line['EndRot'] = {'x': rx, 'y': ry, 'z': 0}
                new_line['Duration'] = spans[i]
                data['Movements'].append(new_line)
            pos = {'x': 0, 'y': h, 'z': -r}
            rot = {'x': 0, 'y': 0, 'z': 0}
            last_pos_rot = (pos, rot)
            continue
        if command[:5] == 'vibro':
            print_log('vibro コマンドを検出')
            dur = b['dur']
            steps = []
            while dur > 0:
                steps.append(min(0.02, dur))
                dur -= 0.02
            for s in steps:
                rx = round(rd()/6, 3)
                ry = round(rd()/6, 3)
                rz = round(rd()/6, 3)
                new_line = create_template()
                vibro_pos_rot = copy.deepcopy(last_pos_rot)
                new_line['StartPos'] = vibro_pos_rot[0]
                new_line['StartRot'] = vibro_pos_rot[1]
                new_line['StartPos']['x'] += rx
                new_line['StartPos']['y'] += ry
                new_line['StartPos']['z'] += rz
                new_line['EndPos'] = new_line['StartPos']
                new_line['EndRot'] = new_line['StartRot']
                new_line['Duration'] = s
                print_log(new_line['StartPos'], new_line['StartRot'])
                data['Movements'].append(new_line)
            continue
        new_line = create_template()
        pos, rot = generate(command)
        last_pos_rot = (pos, rot)
        print_log(pos, rot)
        new_line['StartPos'] = pos
        new_line['StartRot'] = rot
        new_line['EndPos'] = pos
        new_line['EndRot'] = rot
        new_line['Duration'] = b['dur']
        if cnt == 1:
            new_line['Duration'] -= 15/bpm
        data['Movements'].append(new_line)
    elif len(parse) == 2:
        print_log(
            f'2つのスクリプト {parse[0]} と {parse[1] }を確認。startとendに各コマンドを適用します。')
        start_command = parse[0]
        end_command = parse[1]
        new_line = create_template()
        pos, rot = generate(start_command)
        print_log(pos, rot)
        last_pos_rot = (pos, rot)
        new_line['StartPos'] = pos
        new_line['StartRot'] = rot
        pos, rot = generate(end_command)
        print_log(pos, rot)
        last_pos_rot = (pos, rot)
        new_line['EndPos'] = pos
        new_line['EndRot'] = rot
        new_line['Duration'] = b['dur']
        data['Movements'].append(new_line)
    else:
        print_log('スクリプトの解析に失敗しました。')

debug = 0

for m in data['Movements']:
    debug += m['Duration']

print_log('\n全スクリプトの解析を終了しました。')

print_log(f'\nスクリプト占有時間 {int(debug//60)} m {int(debug%60)} s 譜面の長さと一致していれば正常。')

print_log('\nソフト内部でのjsonデータの作成に成功しました。')

target_path = 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Beat Saber\\UserData\\CameraPlus\\Scripts\\Scriptmapper_output.json'
json.dump(data, open(target_path, 'w'), indent=4)

print_log('\nファイルの書き出しを正常に完了しました。')
