from BasicElements import Transform, Pos, Rot
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
        self.lastTransform = Transform(Pos(0, 2, -2), Rot(45, 0, 0), self.fov)
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
        self.logger.log('height コマンドを検出。アバターの視点を以下の値にします。 : ', param)
        self.height = param
        return
    visibleObjects = ['avatar', 'ui', 'wallFrame',  'wall', 'saber', 'notes', 'debris']
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
