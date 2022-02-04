import os
import csv
import json
import pathlib
from random import seed

from BasicElements import Bookmark, Line, Transform, VisibleObject, Logger
from GeneralUtils import format_time, manual_process
from BookmarkUtils import copy_process, fill_process, raw_process
from CommandUtils import env_command, long_command, parse_command
from EaseUtils import ease


class ScriptMapper:
    def __init__(self):
        # system
        self.file_path = None
        self.path_obj = None
        self.logger = None
        self.manual = {}
        # env
        self.bpm = 0
        self.fov = 60
        self.seed = seed(0)
        self.height = 1.5
        self.turnToHead = False
        self.turnToHeadHorizontal = False
        self.visible = VisibleObject()
        # bookmarks
        self.dummyend_grid = 0
        self.raw_b = []
        self.filled_b = []
        self.copied_b = []
        # lines
        self.lines = []
        self.lastTransform = Transform()
        # output
        self.output = None

    def set_file_path(self, file_path):
        self.file_path = file_path
        self.path_obj = pathlib.Path(file_path)
        path_dir = self.path_obj.parent
        logger = Logger(path_dir)
        self.logger = logger

    def confirm_WIP(self):
        isWIP = self.path_obj.parent.parent
        if isWIP.name != 'CustomWIPLevels':
            self.logger.log('WIPフォルダの下にありません。プログラムを終了します。')
            input()
            exit()
        self.logger.log('WIPフォルダの下にあることを確認\n')

    def check_bpm(self):
        path_dir = self.path_obj.parent
        info_path = os.path.join(path_dir, 'info.dat')
        if not os.path.exists(info_path):
            self.logger.log('info.dat が見つかりません。プログラムを終了します。')
            input()
            exit()
        f = open(info_path, 'rb')
        j = json.load(f)
        bpm = j['_beatsPerMinute']
        self.bpm = bpm
        self.logger.log(f'bpmを計測 {self.bpm} \n')

    def make_manual_commands(self):
        path_dir = self.path_obj.parent
        input_path = os.path.join(path_dir, 'input.csv')
        if os.path.exists(input_path):
            self.logger.log('input.csv を確認しました。オリジナルコマンドを追加します。')
            data = csv.DictReader(open(input_path, 'r', encoding='utf-8-sig'))
            manual_process(self, data)
        else:
            self.logger.log('input.csv が見つからないため、オリジナルコマンドは追加されません。\n')

    def make_raw_b(self):
        dummyend_grid = 100
        f = open(self.path_obj, 'r')
        j = json.load(f)
        notes = j['_notes']
        if len(notes) > 0:
            dummyend_grid = notes[-1]['_time']+100
        bookmarks = []
        if '_customData' in j.keys():
            bookmarks = j['_customData']['_bookmarks']
        else:
            bookmarks = j['_bookmarks']
        if len(bookmarks) == 0:
            self.logger.log('この譜面にはブックマークが含まれていません。プログラムを終了します。')
            exit()
        else:
            dummyend_grid = max(dummyend_grid, bookmarks[-1]['_time'] + 100)
        bookmarks.append({'_time': dummyend_grid, '_name': 'dummyend'})
        self.dummyend_grid = dummyend_grid
        self.logger.log(f'ダミーエンドをグリッド {dummyend_grid} に設定。')
        for b in bookmarks:
            raw_process(self, b)

    def make_filled_b(self):
        size = len(self.raw_b)
        for i in range(size-1):
            fill_process(self, i)
        self.filled_b.append(Bookmark(self.dummyend_grid, 'dummy'))

    def make_copied_b(self):
        size = len(self.filled_b)
        for i in range(size-1):
            copy_process(self, i)
        self.copied_b.append(Bookmark(self.dummyend_grid, 'dummy'))

    def calc_duration(self):
        command_b = []
        for b in self.copied_b:
            if b.text[0] == '#':
                continue
            command_b.append(b)
        size = len(command_b)
        for i in range(size-1):
            start = command_b[i].grid
            end = command_b[i+1].grid
            dur_grid = end - start
            command_b[i].duration = dur_grid*60/self.bpm

    def show_bookmarks(self) -> None:
        self.logger.log('\nfill,copyの処理を完了しました。最終的なブックマークは以下になります。')
        self.logger.log('          grid (   time  ) : script')
        cnt = 1
        sum_time = 0
        for b in self.copied_b:
            if b.text[0] == "#":
                self.logger.log(f'    env',
                                f'{b.grid:6.2f}             : {b.text}')
            else:
                self.logger.log(
                    f'{str(cnt).rjust(3)}番目',
                    f'{b.grid:6.2f} ({format_time(sum_time)}) : {b.text}')
                cnt += 1
            sum_time += b.duration

    def parse_bookmarks(self):
        cnt = 0
        sum_time = 0
        for b in self.copied_b:
            if b.text[0] == '#':
                self.logger.log('\n環境コマンドを検出')
                env_command(self, b.text[1:])
                continue
            cnt += 1
            text = b.text
            dur = b.duration
            self.logger.log(f'\n{cnt}番目のスクリプトを確認中...')
            self.logger.log(text)
            self.logger.log(f'grid : {b.grid:6.2f} ({format_time(sum_time)})')
            self.logger.log(f'duration : {dur:.2f}')
            sum_time += dur
            # long command -> process -> skip
            if long_command(self, text, dur):
                continue
            # normal command
            parse = text.split(',')
            if len(parse) == 1:
                parse.append('stop')
                parse.append('False')
            elif len(parse) == 2:
                parse.append('False')
            new_line = Line(dur)
            new_line.turnToHead = self.turnToHead
            new_line.turnToHeadHorizontal = self.turnToHeadHorizontal
            # start
            start_command = parse[0]
            self.logger.log(f'start : {start_command}')
            parse_command(self, new_line.start, start_command)
            self.lastTransform = new_line.start
            # end
            end_command = parse[1]
            self.logger.log(f'end : {end_command}')
            parse_command(self, new_line.end, end_command)
            self.lastTransform = new_line.end
            # ease
            ease_command = parse[2]
            self.logger.log(f'easeTransition : {ease_command}')
            if ease_command != 'False':
                ease(self, dur, ease_command, new_line)
                # data['Movements'].extend(new_lines)
                # print_log(log_text)
                pass
            else:
                self.lines.append(new_line)
            self.logger.log(f'start {new_line.start}')
            self.logger.log(f'end {new_line.end}')

    def render_json(self):
        template = {}
        template['ActiveInPauseMenu'] = True
        template['TurnToHeadUseCameraSetting'] = False
        template['Movements'] = []
        for line in self.lines:
            movement = {}
            movement['StartPos'] = {'x': line.start.pos.x,
                                    'y': line.start.pos.y,
                                    'z': line.start.pos.z,
                                    'FOV': line.start.fov}
            movement['StartRot'] = {'x': line.start.rot.x,
                                    'y': line.start.rot.y,
                                    'z': line.start.rot.z}
            movement['StartHeadOffset'] = {'x': line.startHeadOffset.x,
                                           'y': line.startHeadOffset.y,
                                           'z': line.startHeadOffset.z}
            movement['EndPos'] = {'x': line.end.pos.x,
                                  'y': line.end.pos.y,
                                  'z': line.end.pos.z,
                                  'FOV': line.start.fov}
            movement['EndRot'] = {'x': line.end.rot.x,
                                  'y': line.end.rot.y,
                                  'z': line.end.rot.z}
            movement['EndHeadOffset'] = {'x': line.endHeadOffset.x,
                                         'y': line.endHeadOffset.y,
                                         'z': line.endHeadOffset.z}
            movement['TurnToHead'] = line.turnToHead
            movement['TurnToHeadHorizontal'] = line.turnToHeadHorizontal
            movement['Duration'] = line.duration
            movement['Delay'] = 0
            # movement['VisibleObject'] = {
            #     'avatar': line.visibleObject.avatar,
            #     'ui': line.visibleObject.ui,
            #     'wall': line.visibleObject.wall,
            #     'wallFrame': line.visibleObject.wallFrame,
            #     'saber': line.visibleObject.saber,
            #     'notes': line.visibleObject.notes,
            #     'debris': line.visibleObject.debris,
            # }
            movement['EaseTransition'] = True
            template['Movements'].append(movement)
        self.output = template
        self.logger.log('\nソフト内部でのjsonデータの作成に成功しました。\n')

    def create_file(self):
        custom_map = self.path_obj.parent.name
        not_wip_folder = os.path.join(
            self.path_obj.parents[2], 'CustomLevels', custom_map)
        if os.path.exists(not_wip_folder):
            self.logger.log('カスタムマップに同名のフォルダを確認。こちらにもSongScript.jsonを作成します。\n')
            not_wip_target = os.path.join(not_wip_folder, 'SongScript.json')
            json.dump(self.output, open(not_wip_target, 'w'), indent=4)
            self.logger.log(not_wip_target)
        path_dir = self.path_obj.parent
        target_path = os.path.join(path_dir, 'SongScript.json')
        self.logger.log(target_path)
        json.dump(self.output, open(target_path, 'w'), indent=4)
        self.logger.log('\nファイルの書き出しを正常に完了しました。')
