import os
from datetime import datetime


class Bookmark:
    def __init__(self, grid, text, duration=0):
        self.grid = grid
        self.text = text
        self.duration = duration

    def __str__(self) -> str:
        return (f'{self.grid}:{self.text} dur:{self.duration}')


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

    def __str__(self) -> str:
        return(f'POS:{self.pos}, ROT:{self.rot}, FOV:{self.fov}')


class VisibleObject:

    def __init__(self):
        self.avatar = True
        self.ui = True
        self.wall = True
        self.wallFrame = True
        self.saber = True
        self.notes = True
        self.debris = True


class Line:

    def __init__(self, duration=0):
        self.start = Transform()
        self.end = Transform()
        self.duration = duration
        self.turnToHead = False
        self.turnToHeadHorizontal = False
        self.startHeadOffset = Pos()
        self.endHeadOffset = Pos()
        self.visibleObject = VisibleObject()

    def __str__(self) -> str:
        return (f'{self.duration:6.2f} {self.start} {self.end} ')


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
