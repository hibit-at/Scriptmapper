import copy

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
    move_tmp = copy.deepcopy(template['Movements'][0])
    move_tmp['EaseTransition'] = False
    return move_tmp