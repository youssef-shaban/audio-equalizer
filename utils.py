import altair as alt


def equalizer(mode, signal, points_per_freq, gainsdb_list):
    equalizer_signal = signal.copy()
    for index, slider in enumerate(mode):
        for Range in slider["range"]:
            if gainsdb_list[index] == None:
                gainsdb_list[index] = 0
            equalizer_signal[int(points_per_freq * Range[0]):int(points_per_freq * Range[1])] *= 10 ** (
                        gainsdb_list[index] / 10)
    return equalizer_signal


def initial_time_graph(df):
    return alt.Chart(df).mark_line().encode(
        x=alt.X('time:T', axis=alt.Axis(title='date', labels=False)),
        y=alt.Y('signal:Q', axis=alt.Axis(title='value')),
    ).properties(
        width=600,
        height=230
    ).configure_view(strokeWidth=0).configure_axis(grid=False, domain=False)


def plot_animation(df):
    lines = alt.Chart(df).mark_line().encode(
        x=alt.X('time:T', axis=alt.Axis(title='date', labels=False)),
        y=alt.Y('signal:Q', axis=alt.Axis(title='value')),
    ).properties(
        width=600,
        height=250
    ).configure_view(strokeWidth=0).configure_axis(grid=False, domain=False)
    return lines
