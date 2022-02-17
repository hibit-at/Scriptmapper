import os
from datetime import datetime
from math import degrees, sqrt, atan2


class Bookmark:
    def __init__(self, grid, text, duration=0):
        self.grid = grid
        self.text = text
        self.duration = duration

    def __str__(self) -> str:
        return (f'{self.grid}:{self.text} dur:{self.duration}')


class VisibleObject:

    def __init__(self):
        self.state = {
            'avatar': True,
            'ui': True,
            'wall': True,
            'wallFrame': True,
            'saber': True,
            'notes': True,
            'debris': True,
        }

    def __str__(self) -> str:
        return(str(self.state))


class Pos:

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def unpack(self):
        return (self.x, self.y, self.z)

    def __str__(self) -> str:
        return(f'({self.x:.2f},{self.y:.2f},{self.z:.2f})')


class Rot:

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def unpack(self):
        return (self.x, self.y, self.z)

    def __str__(self) -> str:
        return(f'({self.x:.2f},{self.y:.2f},{self.z:.2f})')


class Transform:
    def __init__(self, pos=Pos(), rot=Rot(), fov=60):
        self.pos = pos
        self.rot = rot
        self.fov = fov

    def set(self, transform):
        self.pos = transform.pos
        self.rot = transform.rot
        self.fov = transform.fov

    def lookat(self, height, lastTransform):
        theta = atan2(self.pos.z, self.pos.x)
        theta = -int(degrees(theta))+270
        r = sqrt(self.pos.x**2+self.pos.z**2)
        angle = int(degrees(atan2(self.pos.y-height, r)))
        self.rot.x = angle
        self.rot.y = theta
        self.rot.z = 0

    def __str__(self) -> str:
        return(f'POS:{self.pos}, ROT:{self.rot}, FOV:{self.fov}')


class Line:

    def __init__(self, duration):
        self.start = Transform()
        self.end = Transform()
        self.duration = duration
        self.turnToHead = False
        self.turnToHeadHorizontal = False
        self.startHeadOffset = Pos()
        self.endHeadOffset = Pos()
        self.visibleDict = None
        self.isNext = False
        self.ease = ''

    def __str__(self) -> str:
        return (f'{self.duration:6.2f} {self.start} {self.end}')


class Logger:

    def __init__(self, path_dir):
        now = str(datetime.now()).replace(':', '_')[:19]
        log_path = os.path.join(path_dir, 'log_latest.txt')
        self.log_path = log_path
        f = open(log_path, 'w', encoding='utf-8')
        f.write(f"logfile at {now}\n\n")

    def log(self, *args):
        str_args = [str(a) for a in args]
        text = ' '.join(str_args)
        print(text)
        f = open(self.log_path, 'a', encoding='utf-8')
        f.write(text+'\n')
