def format_time(sum_time) -> str:
    min = int(sum_time // 60)
    sec = int(sum_time % 60)
    mili = sum_time % 1
    if mili > 0.999:
        mili = 0
        sec += 1
        if sec == 60:
            sec = 0
            min += 1
    mili *= 1000
    return f'{min} m {sec:2.0f} s {mili:4.0f}'


def manual_process(self, data) -> None:
    for d in data:
        if 'fov' not in d:
            d['fov'] = 'env'
            self.logger.log('オリジナルコマンドにfovが設定されていないため、環境FOVを引き継ぎます。')
        self.manual[d['label']] = d
        self.logger.log(d)
    self.logger.log('')
