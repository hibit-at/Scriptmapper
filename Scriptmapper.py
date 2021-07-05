import copy
import csv
import json
import os
import pathlib
import sys
from datetime import date, datetime
from math import atan2, cos, degrees, floor, pi, sin, sqrt
from random import random as rd

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


def print_log(*args):
    str_args = [str(a) for a in args]
    text = ' '.join(str_args)
    print(text)
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(text+'\n')


def create_template():
    move_tmp = copy.deepcopy(template['Movements'][0])
    move_tmp['EaseTransition'] = False
    return move_tmp


def random(r):
    theta = rd()*2*pi
    phi = rd()/4*pi
    angle = atan2(r*sin(phi)-1.5, r)
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


def side(r):
    pos = {'x': r,
           'y': 1.5,
           'z': 0}
    if r >= 0:
        rot = {'x': 0,
               'y': -90,
               'z': 0}
    if r < 0:
        rot = {'x': 0,
               'y': 270,
               'z': 0}
    return pos, rot


def diag(r):
    pos = {'x': r/1.4,
           'y': 3.0,
           'z': -r/1.4}
    if r >= 0:
        rot = {'x': 0,
               'y': -45,
               'z': 0}
    if r < 0:
        rot = {'x': 0,
               'y': 135,
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


def generate(text):
    global last_pos_rot
    if text[:3] == 'def':
        print_log('default コマンドを検出')
        return default()
    elif text[:6] == 'random':
        param = eval(text[6:])
        print_log('random コマンドを検出', param)
        return random(param)
    elif text[:5] == 'front':
        param = eval(text[5:])
        print_log('front コマンドを検出', param)
        return front(param)
    elif text[:4] == 'side':
        param = eval(text[4:])
        print_log('side コマンドを検出', param)
        return side(param)
    elif text[:4] == 'diag':
        param = eval(text[4:])
        print_log('diag コマンドを検出', param)
        return diag(param)
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
            param = eval(text[4:])
        print_log('zoom コマンドを検出', param)
        zoom_pos_rot = copy.deepcopy(last_pos_rot)
        zoom_pos_rot[0]['x'] /= param
        zoom_pos_rot[0]['y'] -= 1.5
        zoom_pos_rot[0]['y'] /= param
        zoom_pos_rot[0]['y'] += 1.5
        zoom_pos_rot[0]['z'] /= param
        return zoom_pos_rot
    elif text[:4] == 'spin':
        print_log('spin コマンドを検出')
        param = eval(text[4:])
        spin_pos_rot = copy.deepcopy(last_pos_rot)
        spin_pos_rot[1]['z'] += param
        return spin_pos_rot
    elif text[:5] == 'screw':
        print_log('screw コマンドを検出')
        param = eval(text[5:])
        screw_pos_rot = copy.deepcopy(last_pos_rot)
        scale = param+1
        screw_pos_rot[0]['x'] /= scale
        screw_pos_rot[0]['y'] -= 1.5
        screw_pos_rot[0]['y'] /= scale
        screw_pos_rot[0]['y'] += 1.5
        screw_pos_rot[0]['z'] /= scale
        screw_pos_rot[1]['z'] += 20*param
        return screw_pos_rot
    elif text[:5] == 'slide':
        param = eval(text[5:])
        print_log('slide コマンドを検出', param)
        slide_pos_rot = copy.deepcopy(last_pos_rot)
        slide_pos_rot[0]['x'] += param
        return slide_pos_rot
    elif text[:5] == 'shift':
        param = eval(text[5:])
        print_log('shift コマンドを検出', param)
        shift_pos_rot = copy.deepcopy(last_pos_rot)
        shift_pos_rot[0]['y'] += param
        return shift_pos_rot
    elif text[:6] == 'before':
        print_log('before コマンドを検出')
        new_pos_rot = copy.deepcopy(last_pos_rot)
        return new_pos_rot
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
                angle = int(degrees(atan2(cy-1.5, r)))
                rot = {'x': angle, 'y': theta, 'z': 0}
            else:
                rot = {'x': float(command['rx']), 'y': float(
                    command['ry']), 'z': float(command['rz'])}
            return pos, rot
        else:
            print_log('コマンドに該当なし、直近の値を返します。')
            return last_pos_rot
# 関数の定義　終わり


# ファイルパスの取得
file_path = sys.argv[1]
path_obj = pathlib.Path(file_path)
path_dir = path_obj.parent

# ログファイルの作成
now = str(datetime.now()).replace(':', '_')[:19]
log_folder_path = os.path.join(path_dir, 'logs')
if not os.path.exists(log_folder_path):
    os.mkdir(log_folder_path)
log_path = os.path.join(log_folder_path, f'log_{now}.txt')
with open(log_path, 'w', encoding='utf-8') as f:
    f.write(f"logfile at {now}\n\n")

# WIPの下にあるか確認
isWIP = path_obj.parent.parent
if isWIP.name != 'CustomWIPLevels':
    print_log('WIPフォルダ直下にありません。プログラムを終了します。')
    wait = input()
    exit()
print_log('WIPフォルダ直下にあることを確認\n')

# BPM計測
info_path = os.path.join(path_dir, 'info.dat')
if not os.path.exists(info_path):
    print_log('info.dat が見つかりません。プログラムを終了します。')
    exit()
f = open(info_path, 'rb')
j = json.load(f)
bpm = j['_beatsPerMinute']
print_log('bpmを計測', bpm, '')

# オリジナルコマンドの登録
manual = {}
input_path = os.path.join(path_dir, 'input.csv')
if os.path.exists(input_path):
    print_log('input.csv を確認しました。オリジナルコマンドを追加します。')
    data = csv.DictReader(open(input_path, 'r', encoding='utf-8-sig'))
    for d in data:
        manual[d['label']] = d
        print_log(d)
else:
    print_log('input.csv が見つからないため、オリジナルコマンドは追加されません。')
print_log('')

# bookmarkの抽出（raw_b）
f = open(file_path, 'r')
j = json.load(f)
notes = j['_notes']
dummyend_grid = notes[-1]['_time']+100
if '_customData' in j.keys():
    raw_b = j['_customData']['_bookmarks']
else:
    raw_b = j['_bookmarks']
raw_b.append({'_time': dummyend_grid, 'text': 'dummyend'})

# 環境コマンドの分離 (sep_b)
print_log('STEP 環境コマンドの分離')
sep_b = []
env_b = []
size = len(raw_b)
for i in range(size-1):
    text = raw_b[i]['_name']
    grid = raw_b[i]['_time']
    if text[0] == '#':
        print_log(f'環境コマンド {text} を検出')
        env_b.append({'time': grid, 'text': text})
    else:
        sep_b.append({'time': grid, 'text': text})
sep_b.append({'_time': dummyend_grid, 'text': 'dummyend'})
print_log('STEPを終了しました。\n')

# 特殊コマンドfillをパース（filled_b）
print_log('STEP fill コマンドの処理')
filled_b = []
size = len(sep_b)
for i in range(size-1):
    text = sep_b[i]['text']
    start_grid = sep_b[i]['time']
    if text[:4] == 'fill':
        param = eval(text.split(',')[0][4:])
        print_log('特殊コマンド fill を検出', param)
        text_pattern = ','.join(text.split(',')[1:])
        span = param
        end_grid = sep_b[i+1]['time']
        print_log(
            f'スクリプト {text_pattern} をグリッド {start_grid} から {end_grid} まで{span}の間隔で敷き詰めます。')
        cnt = 0
        current_grid = start_grid
        while current_grid < end_grid:
            cnt += 1
            filled_b.append({'time': current_grid, 'text': text_pattern})
            print_log(f'{current_grid} : {text_pattern}')
            current_grid += span
        print_log(f'n = {cnt}')
    else:
        filled_b.append({'time': start_grid, 'text': text})
filled_b.append({'time': dummyend_grid, 'text': 'dummyend'})
print_log('STEP を終了しました。\n')

# 特殊コマンドcopyをパース（copied_b）
print_log('STEP copy コマンドの処理')
copied_b = []
size = len(filled_b)
for i in range(size-1):
    text = filled_b[i]['text']
    start_grid = filled_b[i]['time']
    if text[:4] == 'copy':
        param = eval(text.split(',')[0][4:])
        print_log('copy を検出', param)
        text_pattern = ','.join(text.split(',')[1:])
        end_grid = filled_b[i+1]['time']
        t_start_grid = param
        t_end_grid = param + end_grid - start_grid
        print_log(
            f'グリッド{start_grid}～{end_grid}のスクリプトを、グリッド{t_start_grid}～{t_end_grid}からコピーします')
        tmp_b = copy.deepcopy(copied_b)
        for t in tmp_b:
            t_grid = t['time']
            t_text = t['text']
            if t_start_grid <= t_grid and t_grid < t_end_grid:
                append_grid = start_grid + t_grid - t_start_grid
                copied_b.append({'time': append_grid, 'text': t_text})
                print_log(f'{t_grid} -> {append_grid} {t_text}')
    else:
        copied_b.append({'time': start_grid, 'text': text})
copied_b.append({'time': dummyend_grid, 'text': 'dummyend'})
print_log('STEP1 を終了しました。\n')


print_log('STEP3 マップの開始と終了を設定')
final_b = []
size = len(copied_b)
for i in range(size):
    time = copied_b[i]['time']
    text = copied_b[i]['text']
    if i == 0 and time != 0:
        final_b.append({'time': 0, 'text': 'def'})
    final_b.append({'time': time, 'text': text})
print_log(f'開始グリッド {final_b[0]["time"]}')
print_log(f'最後の開始グリッド {final_b[-2]["time"]}')
print_log(f'ダミーエンドグリッド {final_b[-1]["time"]}')

print_log('STEP3を終了しました\n')

# 最終的なグリッド
print_log('特殊コマンドのパースを完了。最終的なスクリプトは以下になります。\n')
for b in final_b:
    grid = b['time']
    text = b['text']
    log_text = f'{grid} : {text}'
    print_log(log_text)

# グリッドを時間に変換
timed_b = []
size = len(final_b)
for i in range(size-1):
    dur = final_b[i+1]['time'] - final_b[i]['time']
    text = final_b[i]['text']
    timed_b.append({'dur': dur*60/bpm, 'text': text})

print_log('\nスクリプトからコマンドへの変換を行います。')
data = copy.deepcopy(template)
data['Movements'] = []
last_pos_rot = default()
cnt = 0
for b in timed_b:
    cnt += 1
    print_log(f'\n{cnt}番目のスクリプト原文を確認中...')
    text = b['text']
    parse = text.split(',')
    if len(parse) == 1:
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
                new_line['StartPos'] = {'x': px, 'y': h, 'z': pz}
                new_line['StartRot'] = {'x': rx, 'y': ry, 'z': 0}
                print_log(
                    f'POS{new_line["StartPos"]} ROT{new_line["StartRot"]}')
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
                print_log(
                    f'POS{new_line["StartPos"]} ROT{new_line["StartRot"]}')
                data['Movements'].append(new_line)
            continue
        print_log(f'単一のスクリプト {parse[0]} を確認。startとendに同じ値を設定します。')
        new_line = create_template()
        pos, rot = generate(command)
        last_pos_rot = (pos, rot)
        print_log(f'POS{pos} ROT{rot}')
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
            f'2つのスクリプト {parse[0]} と {parse[1]}を確認。startとendに各コマンドを適用します。')
        start_command = parse[0]
        end_command = parse[1]
        new_line = create_template()
        pos, rot = generate(start_command)
        print_log(f'POS{pos} ROT{rot}')
        last_pos_rot = (pos, rot)
        new_line['StartPos'] = pos
        new_line['StartRot'] = rot
        pos, rot = generate(end_command)
        print_log(f'POS{pos} ROT{rot}')
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
debug -= data['Movements'][-1]['Duration']

print_log('\n全スクリプトの解析を終了しました。')

print_log(
    f'\nスクリプト占有時間 {int(debug//60)} m {int(debug%60)} s 最後の開始グリッドの再生時間と一致していれば正常。')

print_log('\nソフト内部でのjsonデータの作成に成功しました。')

root_dir = path_dir.parent.parent.parent
target_path = os.path.join(
    root_dir, 'UserData', 'CameraPlus', 'Scripts', 'Scriptmapper_output.json')
print_log(target_path)
json.dump(data, open(target_path, 'w'), indent=4)

print_log('\nファイルの書き出しを正常に完了しました。')
