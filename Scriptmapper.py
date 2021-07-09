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


def get_param(text, length, def_value):
    param = def_value
    if len(text) > length:
        param_word = text[length:]
        check = any([c.isalpha() for c in param_word])
        print(param_word)
        if check:
            print_log(f'パラメータ {param_word} に英字を確認。セキュリティの問題上、プログラムを強制終了します。')
            exit()
        param = eval(param_word)
    return param

def generate(text, last_pos_rot):
    if text[:6] == 'random':
        param = get_param(text, 6, def_value=4)
        print_log('random コマンドを検出', param)
        return random(param)
    if text[:6] == 'center':
        param = get_param(text, 6, def_value=2)
        print_log('center コマンドを検出', param)
        return center(param)
    if text[:4] == 'side':
        param = get_param(text, 4, def_value=2.5)
        print_log('side コマンドを検出', param)
        return side(param)
    if text[:5] == 'diagf':
        param = get_param(text, 5, def_value=4)
        print_log('diagf コマンドを検出', param)
        return diagf(param)
    if text[:5] == 'diagb':
        param = get_param(text, 5, def_value=4)
        print_log('diagb コマンドを検出', param)
        return diagb(param)
    if text[:3] == 'top':
        param = get_param(text, 3, def_value=3)
        print_log('top コマンドを検出', param)
        return top(param)
    if text[:6] == "mirror":
        print_log('mirror コマンドを検出')
        return mirror(last_pos_rot)
    if text[:4] == "zoom":
        param = get_param(text, 4, def_value=2)
        print_log('zoom コマンドを検出', param)
        return zoom(param, last_pos_rot)
    if text[:4] == 'spin':
        param = get_param(text, 4, def_value=20)
        print_log('spin コマンドを検出', param)
        return spin(param, last_pos_rot)
    if text[:5] == 'screw':
        param = get_param(text, 5, def_value=2)
        print_log('screw コマンドを検出')
        return screw(param, last_pos_rot)
    if text[:5] == 'slide':
        param = get_param(text, 5, def_value=1)
        print_log('slide コマンドを検出', param)
        return slide(param, last_pos_rot)
    if text[:5] == 'shift':
        param = get_param(text, 5, def_value=.5)
        print_log('shift コマンドを検出', param)
        return shift(param, last_pos_rot)
    if text[:4] == 'push':
        param = get_param(text, 4, def_value=1)
        print_log('push コマンドを検出', param)
        return push(param, last_pos_rot)
    if text[:4] == 'stop':
        print_log('stop コマンドを検出')
        return stop(last_pos_rot)
    for key in manual.keys():
        length = len(key)
        script = text[:length]
        if script == key:
            print_log(f'オリジナルコマンド {script} を検出')
            command = manual[script]
            return original(command)
    print_log(
        f'！スクリプト {text} はコマンドに変換できません！\n直前の座標を返しますが、意図しない演出になっています。')
    return stop(last_pos_rot)


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
    print_log('')
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

# 環境コマンドの分離（活用未定）
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
last_pos_rot = center(-2)
cnt = 0
for b in timed_b:
    cnt += 1
    print_log(f'\n{cnt}番目のスクリプトを確認中...')
    text = b['text']
    dur = b['dur']
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
    new_line['Duration'] = dur
    ease_command = parse[2]
    print_log(f'EaseTransition : {ease_command}')
    if ease_command != 'False':
        new_lines, log_text = ease(dur, ease_command, new_line)
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

print_log('\n全スクリプトの解析を終了しました。')

print_log(
    f'\nスクリプト占有時間 {int(debug//60)} m {int(debug%60)} s 最後のブックマークの再生時間と一致していれば正常。')

print_log('\nソフト内部でのjsonデータの作成に成功しました。\n')

custom_map = path_obj.parent.name
not_wip_folder = os.path.join(path_obj.parents[2],'CustomLevels',custom_map)
if os.path.exists(not_wip_folder):
    print_log('カスタムマップに同名のフォルダを確認。こちらにもSongScript.jsonを作成します。\n')
    not_wip_target = os.path.join(not_wip_folder,'SongScript.json')
    json.dump(data, open(not_wip_target, 'w'), indent=4)
    print_log(not_wip_target)

target_path = os.path.join(path_dir, 'SongScript.json')
print_log(target_path)
json.dump(data, open(target_path, 'w'), indent=4)

print_log('\nファイルの書き出しを正常に完了しました。')
