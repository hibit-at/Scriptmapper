from BasicElements import Bookmark
from random import random


def raw_process(self, b):
    if b['_name'] == '':
        self.logger.log(
            f'{b["_time"]} 空白のブックマークを検出。デフォルト値として stop を代入します。')
        b['_name'] = 'stop'
    # start check
    if b['_time'] <= 1:
        self.logger.log('スタートから 1 グリッド以内のブックマークはスタート地点にセットします')
        b['_time'] = 0
    self.raw_b.append(Bookmark(b['_time'], b['_name'], 0))


def fill_process(self, i):
    text = self.raw_b[i].text
    start_grid = self.raw_b[i].grid
    if i == 0 and start_grid != 0:
        # ans.append({'time': 0, 'text': 'center-2'})
        self.filled_b.append(Bookmark(0, 'center-2'))
        self.logger.log(
            '開始位置（グリッド0）にブックマークがないため、スクリプト center-2 を挿入しました。')
    if text[:4] == 'fill':
        if text.split(',')[0] == 'fill':
            self.logger.log('! fill にパラメータが指定されていません。')
            return
        param = eval(text.split(',')[0][4:])
        self.logger.log(f'fill を検出  パラメータ  {str(param)}')
        orig_text_pattern = ','.join(text.split(',')[1:])
        span = param
        end_grid = self.raw_b[i+1].grid
        self.logger.log(
            f'スクリプト {orig_text_pattern} をグリッド {start_grid} から',
            f'{end_grid} の直前まで {span} の間隔で敷き詰めます。')
        cnt = 0
        current_grid = start_grid
        while current_grid < end_grid:
            # "!"と'?'を変数に
            text_pattern = orig_text_pattern.replace('!', str(cnt))
            text_pattern = text_pattern.replace('?', str(random()))
            cnt += 1
            self.filled_b.append(Bookmark(current_grid, text_pattern))
            self.logger.log(f'{current_grid} : {text_pattern}')
            current_grid += span
        self.logger.log(f'n = {cnt}')
    else:
        self.filled_b.append(self.raw_b[i])


def copy_process(self, i):
    text = self.filled_b[i].text
    start_grid = self.filled_b[i].grid
    if i == 0 and start_grid != 0:
        self.copied_b.append(Bookmark(0, 'center-2'))
        self.logger.log(
            '開始位置（グリッド0）にブックマークがないため、スクリプト center-2 を挿入しました。')
    if text[:4] == 'copy':
        if text.split(',')[0] == 'copy':
            self.logger.log('! copy にパラメータが指定されていません。')
            return
        param = eval(text.split(',')[0][4:])
        self.logger.log(f'copy を検出  パラメータ  {str(param)}')
        end_grid = self.filled_b[i+1].grid
        t_start_grid = param
        t_end_grid = param + end_grid - start_grid
        self.logger.log(
            f'グリッド {start_grid}～{end_grid} のスクリプトを',
            f'グリッド {t_start_grid}～{t_end_grid} からコピーします')
        tmp = self.copied_b
        for t in tmp:
            t_grid = t.grid
            t_text = t.text
            if t_start_grid <= t_grid and t_grid < t_end_grid:
                append_grid = start_grid + t_grid - t_start_grid
                self.copied_b.append(Bookmark(append_grid, t_text))
                self.logger.log(f'{t_grid} -> {append_grid} {t_text}')
    else:
        self.copied_b.append(self.filled_b[i])
