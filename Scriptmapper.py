import csv
import json
import os
import pathlib
import sys
from copy import deepcopy
from datetime import datetime, time

from commands import *
from utils import create_template, grid_parse, template

from random import seed

# 関数の定義


def print_log(*args):
    str_args = [str(a) for a in args]
    text = ' '.join(str_args)
    print(text)
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(text+'\n')


def get_param(text, length, def_value):
    param = def_value
    if len(text) > length:
        param_word = text[length:]
        check = any([c.isalpha() for c in param_word])
        if check:
            print_log(f'パラメータ {param_word} に英字を確認。セキュリティの問題上、プログラムを強制終了します。')
            exit()
        param = eval(param_word)
    return param


def generate(text, last_pos_rot, height=1.5):
    for key in manual.keys():
        if text == key:
            print_log(f'オリジナルコマンド {key} を検出')
            command = manual[key]
            return original(command, height)
    for c in command_values:
        if text.startswith(c):
            leng = len(c)
            param = get_param(text, leng, def_value=command_values[c])
            print_log(f'{c} コマンドを検出　パラメータ：', param)
            func = eval(c)
            ans = func(param, last_pos_rot, fov, height)
            # ans[0]['FOV'] = fov
            return ans
    print_log(
        f'！スクリプト {text} はコマンドに変換できません！\n直前の座標を返しますが、意図しない演出になっています。')
    return stop('-', last_pos_rot, height)


def env_command(text):
    global fov
    global height
    global last_pos_rot
    global isHead
    if text[:3] == 'fov':
        param = 60
        if len(text) > 3:
            param_word = text[3:]
            check = any([c.isalpha() for c in param_word])
            if check:
                print_log(
                    f'パラメータ {param_word} に英字を確認。セキュリティの問題上、プログラムを強制終了します。')
                exit()
            param = eval(param_word)
        print_log('fov コマンドを検出。FOVを以下の値にします。', param)
        fov = param
    elif text[:4] == 'seed':
        param = 0
        if len(text) > 4:
            param_word = text[4:]
            check = any([c.isalpha() for c in param_word])
            if check:
                print_log(
                    f'パラメータ {param_word} に英字を確認。セキュリティの問題上、プログラムを強制終了します。')
                exit()
            param = eval(param_word)
        print_log('seed コマンドを検出。ランダムシードを以下の値にします。：', param)
        seed(param)
        last_pos_rot = center(-2, 'dummy', fov, height)  # 直前の座標をリセット
    elif text[:4] == 'head':
        print_log('head コマンドを検出。HMD追従モードを切り替えます。', isHead, '->', not isHead)
        isHead = not isHead
    elif text[:6] == 'height':
        param = 1.5
        if len(text) > 6:
            param_word = text[6:]
            check = any([c.isalpha() for c in param_word])
            if check:
                print_log(
                    f'パラメータ {param_word} に英字を確認。セキュリティの問題上、プログラムを強制終了します。')
                exit()
            param = eval(param_word)
        print_log('height コマンドを検出。アバターの身長を以下の値にします。：', param)
        height = param
    else:
        print_log('！有効な環境コマンドを検出できません！')


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
    print_log('WIPフォルダの下にありません。プログラムを終了します。')
    wait = input()
    exit()
print_log('WIPフォルダの下にあることを確認\n')

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
        if 'fov' not in d:
            d['fov'] = 60
            print_log('オリジナルコマンドにfovが設定されていないため、60 を設定しました。')
        manual[d['label']] = d
        print_log(d)
    print_log('')
else:
    print_log('input.csv が見つからないため、オリジナルコマンドは追加されません。\n')

# bookmarkの抽出（raw_b）
dummyend_grid = 100
f = open(file_path, 'r')
j = json.load(f)
notes = j['_notes']
if len(notes) > 0:
    dummyend_grid = notes[-1]['_time']+100
if '_customData' in j.keys():
    raw_b = j['_customData']['_bookmarks']
else:
    raw_b = j['_bookmarks']
if len(raw_b) == 0:
    print_log('この譜面にはブックマークが含まれていません。プログラムを終了します。')
    exit()
else:
    dummyend_grid = max(dummyend_grid, raw_b[-1]['_time'] + 100)
raw_b.append({'_time': dummyend_grid, 'text': 'dummyend'})
print_log(f'ダミーエンドをグリッド {dummyend_grid} に設定。')

# ダミーエンドを追加
scripts = []
size = len(raw_b)
for i in range(size-1):
    text = raw_b[i]['_name']
    grid = raw_b[i]['_time']
    scripts.append({'time': grid, 'text': text})
scripts.append({'time': dummyend_grid, 'text': 'dummyend'})

# fillの処理
scripts, log_text = grid_parse('fill', scripts, dummyend_grid)
print_log(log_text)
print_log('fill の処理が正常に終了しました。\n')
# copyの処理
scripts, log_text = grid_parse('copy', scripts, dummyend_grid)
print_log(log_text)
print_log('copy の処理が正常に終了しました。\n')


# 最終的なグリッド
cnt = 0
print_log('fill,copy の処理を完了。最終的なスクリプトは以下になります。\n')
print_log('   　　 　 grid : script')
for s in scripts:
    grid = s['time']
    text = s['text']
    if text[0] == "#":
        log_text = f'    env　         {text}'
    else:
        log_text = f'{str(cnt).rjust(3)}番目　{grid:6.2f} : {text}'
        cnt += 1
    print_log(log_text)

# 環境コマンドの分離
command_scripts = []
env_b = []
size = len(scripts)
for s in scripts:
    text = s['text']
    grid = s['time']
    if len(text) > 0 and text[0] == '#':
        env_b.append({'start': grid, 'text': text})
    else:
        command_scripts.append({'start': grid, 'text': text})

# durationを計算
timed_b = []
size = len(command_scripts)
for i in range(size-1):
    start = command_scripts[i]['start']
    dur = command_scripts[i+1]['start'] - command_scripts[i]['start']
    text = command_scripts[i]['text']
    timed_b.append({'start': start, 'dur': dur*60/bpm, 'text': text})

# 環境コマンドとのマージ
timed_b.extend(env_b)
timed_b = sorted(timed_b, key=lambda x: x['start'])

# スクリプト化
print_log('\nスクリプトからコマンドへの変換を行います。')
data = deepcopy(template)
data['Movements'] = []
height = 1.5
last_pos_rot = center(-2, 'dummy', 60, height)
seed(0)
isHead = False
fov = 60
cnt = 0
sum_dur = 0
for b in timed_b:
    if b['text'][0] == '#':
        print_log('\n環境コマンドを検出')
        text = b['text'][1:]
        env_command(text)
        continue
    cnt += 1
    print_log(f'\n{cnt}番目のスクリプトを確認中...')
    print_log('grid :', b['start'],
              f'({int(sum_dur//60)} m {int(sum_dur%60)} s)')
    text = b['text']
    dur = b['dur']
    print_log('duration :', dur)
    sum_dur += dur
    # rotate
    if text[:6] == 'rotate':
        print_log(text)
        print_log('rotate コマンドを確認')
        if any([c.isalpha() for c in text[6:]]):
            print_log(f'パラメータ {text[6:]} に英字を確認。セキュリティの問題上、プログラムを強制終了します。')
            exit()
        new_lines, log_text = rotate(dur, text)
        data['Movements'].extend(new_lines)
        print_log(log_text)
        continue
    # vibro
    if text[:5] == 'vibro':
        print_log(text)
        param = get_param(text, 5, def_value=1/4)
        print_log('vibro コマンドを確認 ', param)
        new_lines, log_text = vibro(dur, bpm, param, last_pos_rot)
        data['Movements'].extend(new_lines)
        print_log(log_text)
        continue
    parse = text.split(',')
    if len(parse) == 1:
        parse.append('stop')
        parse.append('False')
    elif len(parse) == 2:
        parse.append('False')
    new_line = create_template(isHead, height)
    start_command = parse[0]
    print_log(f'start : {start_command}')
    pos, rot = generate(start_command, last_pos_rot, height)
    last_pos_rot = (pos, rot)
    # print_log('臨時ログ', last_pos_rot)
    new_line['StartPos'] = pos
    new_line['StartRot'] = rot
    end_command = parse[1]
    print_log(f'end : {end_command}')
    pos, rot = generate(end_command, last_pos_rot, height)
    last_pos_rot = (pos, rot)
    new_line['EndPos'] = pos
    new_line['EndRot'] = rot
    new_line['Duration'] = dur
    ease_command = parse[2]
    print_log(f'EaseTransition : {ease_command}')
    if ease_command != 'False':
        new_lines, log_text = ease(dur, ease_command, new_line, isHead, height)
        data['Movements'].extend(new_lines)
        print_log(log_text)
    else:
        data['Movements'].append(new_line)
    print_log(f'start POS{new_line["StartPos"]} ROT{new_line["StartRot"]}')
    print_log(f'end POS{new_line["EndPos"]} ROT{new_line["EndRot"]}')

data['Movements'][0]['Duration'] -= 0.04  # モタるよりも走った方が良いので安全側のオフセット

debug = 0
for m in data['Movements']:
    debug += m['Duration']
debug -= data['Movements'][-1]['Duration']
debug += 0.04

print_log('\n全スクリプトの解析を終了しました。')

print_log(
    f'\nスクリプト占有時間 {int(debug//60)} m {debug%60} s 最後のブックマークの再生時間と一致していれば正常。')

print_log('\nソフト内部でのjsonデータの作成に成功しました。\n')

custom_map = path_obj.parent.name
not_wip_folder = os.path.join(path_obj.parents[2], 'CustomLevels', custom_map)
if os.path.exists(not_wip_folder):
    print_log('カスタムマップに同名のフォルダを確認。こちらにもSongScript.jsonを作成します。\n')
    not_wip_target = os.path.join(not_wip_folder, 'SongScript.json')
    json.dump(data, open(not_wip_target, 'w'), indent=4)
    print_log(not_wip_target)

target_path = os.path.join(path_dir, 'SongScript.json')
print_log(target_path)
json.dump(data, open(target_path, 'w'), indent=4)

print_log('\nファイルの書き出しを正常に完了しました。')
