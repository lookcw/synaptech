import numpy as np


def fsl_settings():
    ls = range(2, 10, 5)
    ps = np.arange(0.49)
    ms = [10]
    ss = [1]
    windows = [(10,100),(100,500)]
    regions = [True]
    configs = []
    for l in ls:
        for p in ps:
            for m in ms:
                for s in ss:
                    for window in windows:
                        configs.append({
                            'l': l,
                            'm': m,
                            'p': p,
                            's': s,
                            'x': window[0],
                            'w': window[1],
                            'compress': False
                        })
    optimal = [{
        'l': 4,
        'm': 10,
        'p': 0.049,
        's': 1,
        'x': 200,
        'w': 2000,
        'compress': False,
    }
    ]
    return optimal

def pearson_settings():
    PEARSON_1 = {
        'compress': False,
        'regions': False
    }
    return [PEARSON_1]

def domfreq_settings():
    lower_bounds = [2]
    upper_bounds = [10]
    configs = []
    for lower_bound in lower_bounds:
        for upper_bound in upper_bounds:
            configs.append({'lower_bound':lower_bound,'upper_bound':upper_bound})
    return configs