import csv
import json
import os
import pathlib
import sys
from copy import deepcopy
from datetime import datetime

from commands import *
from utils import create_template, grid_parse, template


# 関数の定義
def print_log(*args):
    str_args = [str(a) for a in args]
    text = ' '.join(str_args)
    print(text)
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(text+'\n')


def generate(text, last_pos_rot):
    if text[:3] == 'def':
        print_log('default コマンドを検出')
        return default()
    elif text[:6] == 'random':
        param = 4.0  # init
        if len(text) > 6:
            param = eval(text[6:])
        print_log('random コマンドを検出', param)
        return random(param)
    elif text[:5] == 'front':
        param = 2.0  # init
        if len(text) > 5:
            param = eval(text[5:])
        print_log('front コマンドを検出', param)
        return front(param)
    elif text[:4] == 'side':
        param = 2.5  # init
        if len(text) > 4:
            param = eval(text[4:])
        print_log('side コマンドを検出', param)
        return side(param)
    elif text[:4] == 'diag':
        param = 4  # init
        if len(text) > 4:
            param = eval(text[4:])
        print_log('diag コマンドを検出', param)
        return diag(param)
    elif text[:3] == 'top':
        param = 3  # init
        if len(text) > 3:
            param = eval(text[3:])
        print_log('top コマンドを検出', param)
    elif text[:6] == "mirror":
        print_log('mirror コマンドを検出')
        return mirror(last_pos_rot)
    elif text[:4] == "zoom":
        param = 2.0  # init
        if len(text) > 4:
            param = eval(text[4:])
        print_log('zoom コマンドを検出', param)
        return zoom(param, last_pos_rot)
    elif text[:4] == 'spin':
        param = 20
        if len(text) > 4:
            param = eval(text[4:])
        print_log('spin コマンドを検出', param)
        return spin(param, last_pos_rot)
    elif text[:5] == 'screw':
        param = 2.0
        if len(text) > 5:
            param = eval(text[5:])
        print_log('screw コマンドを検出')
        return screw(param, last_pos_rot)
    elif text[:5] == 'slide':
        param = 1
        if len(text) > 5:
            param = eval(text[5:])
        print_log('slide コマンドを検出', param)
        return slide(param, last_pos_rot)
    elif text[:5] == 'shift':
        param = .5
        if len(text) > 5:
            param = eval(text[5:])
        print_log('shift コマンドを検出', param)
        return shift(param, last_pos_rot)
    elif text[:4] == 'push':
        param = 1
        if len(text) > 4:
            param = eval(text[4:])
        print_log('push コマンドを検出', param)
    elif text[:6] == 'before':
        print_log('before コマンドを検出')
        return before(last_pos_rot)
    else:
        if text in manual.keys():
            print_log(f'オリジナルコマンド {text} を検出')
            command = manual[text]
            return original(command)
        else:
            print_log('コマンドに該当なし、直近の値を返します。')
            return before(last_pos_rot)


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
    print_log('input.csv が見つからないため、オリジナルコマンドは追加されません。\n')

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

# 環境コマンドの分離
scripts = []
env_b = []
size = len(raw_b)
for i in range(size-1):
    text = raw_b[i]['_name']
    grid = raw_b[i]['_time']
    if len(text) > 0 and text[0] == '#':
        print_log(f'環境コマンド {text} を検出')
        env_b.append({'time': grid, 'text': text})
    else:
        scripts.append({'time': grid, 'text': text})
scripts.append({'_time': dummyend_grid, 'text': 'dummyend'})

# fillの処理
scripts, log_text = grid_parse('fill', scripts, dummyend_grid)
print_log(log_text)
print_log('fill の処理が正常に終了しました。')
# copyの処理
scripts, log_text = grid_parse('copy', scripts, dummyend_grid)
print_log(log_text)
print_log('copy の処理が正常に終了しました。')

# 最終的なグリッド
cnt = 0
print_log('特殊コマンドのパースを完了。最終的なスクリプトは以下になります。\n')
print_log('   　　 　 grid : script')
for s in scripts:
    cnt += 1
    grid = s['time']
    text = s['text']
    log_text = f'{str(cnt).rjust(3)}番目　{grid:6.2f} : {text}'
    print_log(log_text)

# グリッドを時間に変換
timed_b = []
size = len(scripts)
for i in range(size-1):
    dur = scripts[i+1]['time'] - scripts[i]['time']
    text = scripts[i]['text']
    timed_b.append({'dur': dur*60/bpm, 'text': text})

print_log('\nスクリプトからコマンドへの変換を行います。')
data = deepcopy(template)
data['Movements'] = []
last_pos_rot = default()
cnt = 0
for b in timed_b:
    cnt += 1
    print_log(f'\n{cnt}番目のスクリプトを確認中...')
    text = b['text']
    dur = b['dur']
    if text[:6] == 'rotate':
        print_log('rotate コマンドを確認')
        new_lines = rotate(dur, text)
        for n in new_lines:
            pos = n['StartPos']
            rot = n['StartRot']
            print_log(f'start POS{n["StartPos"]} ROT{n["StartRot"]}')
            print_log(f'end POS{n["EndPos"]} ROT{n["EndRot"]}')
            data['Movements'].append(n)
        continue
    if text[:5] == 'vibro':
        param = 1/4
        if len(text) > 5:
            param = eval(text[5:])
        print_log('vibro コマンドを確認 ', param)
        new_lines = vibro(dur, bpm, param, last_pos_rot)
        for n in new_lines:
            pos = n['StartPos']
            rot = n['StartRot']
            print_log(f'start POS{n["StartPos"]} ROT{n["StartRot"]}')
            print_log(f'end POS{n["EndPos"]} ROT{n["EndRot"]}')
            data['Movements'].append(n)
        continue
    parse = text.split(',')
    if len(parse) == 1:
        parse.append('before')
    new_line = create_template()
    start_command = parse[0]
    print_log(f'start : {start_command}')
    pos, rot = generate(start_command, last_pos_rot)
    last_pos_rot = (pos, rot)
    new_line['StartPos'] = pos
    new_line['StartRot'] = rot
    end_command = parse[1]
    print_log(f'end : {end_command}')
    pos, rot = generate(end_command, last_pos_rot)
    last_pos_rot = (pos, rot)
    new_line['EndPos'] = pos
    new_line['EndRot'] = rot
    new_line['Duration'] = b['dur']
    print_log(f'start POS{new_line["StartPos"]} ROT{new_line["StartRot"]}')
    print_log(f'end POS{new_line["EndPos"]} ROT{new_line["EndRot"]}')
    data['Movements'].append(new_line)

debug = 0
for m in data['Movements']:
    debug += m['Duration']
debug -= data['Movements'][-1]['Duration']

print_log('\n全スクリプトの解析を終了しました。')

print_log(
    f'\nスクリプト占有時間 {int(debug//60)} m {int(debug%60)} s 最後の開始グリッドの再生時間と一致していれば正常。')

print_log('\nソフト内部でのjsonデータの作成に成功しました。')

target_path = os.path.join(path_dir, 'SongScript.json')
print_log(target_path)
json.dump(data, open(target_path, 'w'), indent=4)

print_log('\nファイルの書き出しを正常に完了しました。')
