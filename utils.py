mode1= [
    {
        "label":"80Hz",
        "range":[(0,80)]
    },
    {
        "label":"240Hz",
        "range":[(81,240)]
    },
    {
        "label":"500Hz",
        "range":[(241,500)]
    },
    {
        "label":"800Hz",
        "range":[(501,800)]
    },
    {
        "label":"1.4KHz",
        "range":[(801,1400)]
    },
    {
        "label":"2KHz",
        "range":[(1401,2000)]
    },
    {
        "label":"3.5KHz",
        "range":[(2001,3500)]
    },
    {
        "label":"6KHz",
        "range":[(3501,6000)]
    },
    {
        "label":"9KHz",
        "range":[(6001,9000)]
    },
    {
        "label":"14KHz",
        "range":[(9001,14000)]
    },
]


def equalizer(mode, signal, points_per_freq, gainsdb_list):
    equalizer_signal=signal.copy()
    for index,slider in enumerate(mode):
        for Range in slider["range"]:
            if gainsdb_list[index]==None:
                gainsdb_list[index]=0
            equalizer_signal[int(points_per_freq*Range[0]):int(points_per_freq*Range[1])]*= 10**(gainsdb_list[index]/10)
    return equalizer_signal