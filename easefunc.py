from math import cos, pi, sin, sqrt

# Reference: https://easings.net/

easetypes = ['InSine','OutSine','InOutSine','InCubic','OutCubic','InOutCubic',
             'InQuint','OutQuint','InOutQuint','InCirc','OutCirc','InOutCirc',
             'InElastic','OutElastic','InOutElastic','InQuad','OutQuad','InOutQuad',
             'InQuart','OutQuart','InOutQuart','InExpo','OutExpo','InOutExpo',
             'InBack','OutBack','InOutBack','InBounce','OutBounce','InOutBounce']

def InSine(t):
    return 1 - cos((t * pi) / 2)

def OutSine(t):
  return sin((t * pi) / 2)

def InOutSine(t):
    return -(cos(pi * t) - 1) / 2

def InCubic(t):
    return t * t * t

def OutCubic(t):
    return 1 - pow(1 - t, 3)

def InOutCubic(t):
    return 4 * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 3) / 2

def InQuint(t):
    return t * t * t * t * t

def OutQuint(t):
    return 1 - pow(1 - t, 5)

def InOutQuint(t):
    return 16 * t * t * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 5) / 2

def InCirc(t):
    return 1 - sqrt(1 - pow(t, 2))

def OutCirc(t):
    return sqrt(1 - pow(t - 1, 2))

def InOutCirc(t):
    return (1 - sqrt(1 - pow(2 * t, 2))) / 2 if t < 0.5 else (sqrt(1 - pow(-2 * t + 2, 2)) + 1) / 2

def InElastic(t):
    c4 = (2 * pi) / 3
    if t==0:
        return 0
    elif t==1:
        return 1
    else:
        return -pow(2, 10 * t - 10) * sin((t * 10 - 10.75) * c4)

def OutElastic(t):
    c4 = (2 * pi) / 3
    if t==0:
        return 0
    elif t==1:
        return 1
    else:
        return pow(2, -10 * t) * sin((t * 10 - 0.75) * c4) + 1

def InOutElastic(t):
    c5 = (2 * pi) / 4.5
    if t==0:
        return 0
    elif t==1:
        return 1
    elif t < 0.5:
        return -(pow(2, 20 * t - 10) * sin((20 * t - 11.125) * c5)) / 2
    else:
        return (pow(2, -20 * t + 10) * sin((20 * t - 11.125) * c5)) / 2 + 1

def InQuad(t):
    return t * t

def OutQuad(t):
    return 1 - (1 - t) * (1 - t)

def InOutQuad(t):
    return 2 * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 2) / 2

def InQuart(t):
    return t * t * t * t

def OutQuart(t):
    return 1 - pow(1 - t, 4)

def InOutQuart(t):
    return 8 * t * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 4) / 2

def InExpo(t):
    return 0 if t == 0 else pow(2, 10 * t - 10)

def OutExpo(t):
    return 1 if t == 1 else 1 - pow(2, -10 * t)

def InOutExpo(t):
    if t==0:
        return 0
    elif t==1:
        return 1
    elif t < 0.5:
        return pow(2, 20 * t - 10) / 2
    else:
        return (2 - pow(2, -20 * t + 10)) / 2

def InBack(t):
    c1 = 1.70158
    c3 = c1 + 1
    return c3 * t * t * t - c1 * t * t

def OutBack(t):
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2)

def InOutBack(t):
    c1 = 1.70158
    c2 = c1 * 1.525
    return (pow(2 * t, 2) * ((c2 + 1) * 2 * t - c2)) / 2 if t < 0.5 else (pow(2 * t - 2, 2) * ((c2 + 1) * (t * 2 - 2) + c2) + 2) / 2

def InBounce(t):
    return 1 - OutBounce(1 - t)

def OutBounce(t):
    n1 = 7.5625
    d1 = 2.75
    if t < (1 / d1):
        return n1 * t * t
    elif t < (2 / d1):
        return n1 * (t - 1.5 / d1)**2 + 0.75
    elif t < (2.5 / d1):
        return n1 * (t - 2.25 / d1)**2 + 0.9375
    else:
        return n1 * (t - 2.625 / d1)**2 + 0.984375

def InOutBounce(t):
    return (1 - OutBounce(1 - 2 * t)) / 2 if t < 0.5 else (1 + OutBounce(2 * t - 1)) / 2