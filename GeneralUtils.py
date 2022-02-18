from math import degrees, atan2, sqrt

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
        try:
            float(d['fov'])
        except ValueError:
            self.logger.log('fov に数値以外が入力されているため、環境FOVを引き継ぎます。')
            d['fov'] = 'env'
        if d['lookat'].lower() == 'true':
            px = float(d['px'])
            py = float(d['py'])
            pz = float(d['pz'])
            theta = atan2(pz, px)
            theta = -int(degrees(theta))+270
            r = sqrt(px**2+pz**2)
            angle = int(degrees(atan2(py-1.5, r)))
            d['rx'] = angle
            d['ry'] = theta
            d['rz'] = 0
        if 'fov' not in d:
            d['fov'] = 'env'
            self.logger.log('オリジナルコマンドにfovが設定されていないため、環境FOVを引き継ぎます。')
        inits = ['px','px','pz','rx','ry','rz']
        for init in inits:
            if d[init] == '':
                d[init] = 0
        self.manual[d['label']] = d
        self.logger.log(d)
    self.logger.log('')


def get_param(self, text, length, def_value) -> float:
    param = def_value
    if len(text) > length:
        param_word = text[length:]
        check = any([c.isalpha() for c in param_word])
        if check:
            self.logger.log(f'パラメータ {param_word} に英字を確認。' +
                            f'セキュリティの問題上、プログラムを強制終了します。')
            input()
            exit()
        param = eval(param_word)
    return param
