from GeneralUtils import get_param


def env_command(self, text) -> None:
    if text[:3] == 'fov':
        param = get_param(self, text, 3, 60)
        self.logger.log('fov コマンドを検出。FOVを以下の値にします。 : ', param)
        self.fov = param
        return
    if text[:4] == 'seed':
        param = get_param(self, text, 4, 0)
        self.logger.log('seed コマンドを検出。ランダムシードを以下の値にします。 : ', param)
        self.seed(param)
        # center-2 as default
        return
    if text[:4] == 'head':
        self.logger.log('head コマンドを検出。HMD追従モードを切り替えます。',
                        self.turnToHead, '->', not self.turnToHead)
        self.turnToHead = not self.turnToHead
        return
    if text[:7] == 'horizo':
        self.logger.log('horizo コマンドを検出。HMD追従モードを切り替えます。',
                        self.turnToHeadHorizontal, '->', not self.turnToHeadHorizontal)
        self.turnToHeadHorizontal = not self.turnToHeadHorizontal
        return
    if text[:6] == 'height':
        param = get_param(self, text, 6, 1.5)
        self.logger.log('height コマンドを検出。アバターの身長（目の高さ）を以下の値にします。 : ', param)
        self.height = param
        return
    if text[:3] == 'def':
        param = text[3:]
        if param[0] == ',' or param[0] == ' ':
            param = param[1:]
        self.logger.log(f'def コマンドを検出。現在の位置・角度をオリジナルコマンド {param} とします。')
        add_command = {}
        add_command['px'] = self.lastTransform.pos.x
        add_command['py'] = self.lastTransform.pos.y
        add_command['pz'] = self.lastTransform.pos.z
        add_command['rx'] = self.lastTransform.rot.x
        add_command['ry'] = self.lastTransform.rot.y
        add_command['rz'] = self.lastTransform.rot.z
        add_command['fov'] = self.lastTransform.fov
        add_command['lookat'] = 'false'
        self.manual[param] = add_command
        self.logger.log(add_command)
        return
    if text[:6] == 'offset':
        param = get_param(self, text, 6, 0)
        self.logger.log(f'offset コマンドを検出。次のコマンドのオフセット期間を {param} 秒短縮します。')
        self.offset = param
        return
    visibleObjects = ['avatar', 'ui', 'wallFrame',
                      'wall', 'saber', 'notes', 'debris']
    for visibleObject in visibleObjects:
        leng = len(visibleObject)
        if text[:leng] == visibleObject:
            self.logger.log(f'{visibleObject} コマンドを検出。')
            param = text[leng:]
            if param.upper() == 'ON':
                # exec(f'self.visibleObject.{visibleObject} = True')
                self.visibleObject.state[visibleObject] = True
                self.logger.log(f'{visibleObject} を ON にします。')
                self.logger.log(self.visibleObject)
            elif param.upper() == 'OFF':
                # exec(f'self.visibleObject.{visibleObject} = False')
                self.visibleObject.state[visibleObject] = False
                self.logger.log(f'{visibleObject} を OFF にします。')
                self.logger.log(self.visibleObject)
            else:
                self.logger.log('パラメータを検出できません。')
            return
    self.logger.log('! 有効な環境コマンドを検出できません !')
