def equalizer(mode, signal, points_per_freq, gainsdb_list):
    equalizer_signal=signal.copy()
    for index,slider in enumerate(mode):
        for Range in slider["range"]:
            if gainsdb_list[index]==None:
                gainsdb_list[index]=0
            equalizer_signal[int(points_per_freq*Range[0]):int(points_per_freq*Range[1])]*= 10**(gainsdb_list[index]/10)
    return equalizer_signal