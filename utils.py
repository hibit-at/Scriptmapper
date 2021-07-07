from copy import deepcopy

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

def create_template():
    move_tmp = deepcopy(template['Movements'][0])
    move_tmp['EaseTransition'] = False
    return move_tmp

def grid_parse(mode, origin, dummyend_grid):
    ans = []
    log_texts = []
    size = len(origin)
    for i in range(size-1):
        text = origin[i]['text']
        start_grid = origin[i]['time']
        if i == 0 and start_grid != 0:
            ans.append({'time': 0, 'text': 'back'})
            log_texts.append('開始位置（グリッド0）にブックマークがないため、backを挿入しました。')
        if mode == 'fill' and text[:4] == 'fill':
            if text.split(',')[0] == 'fill':
                log_texts.append('！fill にパラメータが指定されていません。')
                continue
            param = eval(text.split(',')[0][4:])
            log_texts.append('fill を検出')
            log_texts.append(str(param))
            text_pattern = ','.join(text.split(',')[1:])
            span = param
            end_grid = origin[i+1]['time']
            log_texts.append(f'スクリプト {text_pattern} をグリッド {start_grid} から {end_grid} まで{span}の間隔で敷き詰めます。')
            cnt = 0
            current_grid = start_grid
            while current_grid < end_grid:
                cnt += 1
                ans.append({'time': current_grid, 'text': text_pattern})
                log_texts.append(f'{current_grid} : {text_pattern}')
                current_grid += span
            log_texts.append(f'n = {cnt}')
        elif mode == 'copy' and text[:4] == 'copy':
            if text.split(',')[0] == 'copy':
                log_texts.append('！copy にパラメータが指定されていません。')
                continue
            param = eval(text.split(',')[0][4:])
            log_texts.append('copy を検出')
            log_texts.append(str(param))
            text_pattern = ','.join(text.split(',')[1:])
            end_grid = origin[i+1]['time']
            t_start_grid = param
            t_end_grid = param + end_grid - start_grid
            log_texts.append(f'グリッド{start_grid}～{end_grid}のスクリプトを、グリッド{t_start_grid}～{t_end_grid}からコピーします')
            tmp = deepcopy(ans)
            for t in tmp:
                t_grid = t['time']
                t_text = t['text']
                if t_start_grid <= t_grid and t_grid < t_end_grid:
                    append_grid = start_grid + t_grid - t_start_grid
                    ans.append({'time': append_grid, 'text': t_text})
                    log_texts.append(f'{t_grid} -> {append_grid} {t_text}')
        else:
            ans.append({'time': start_grid, 'text': text})
    ans.append({'time': dummyend_grid, 'text': 'dummyend'})
    text = '\n'.join(log_texts)
    return ans, text
