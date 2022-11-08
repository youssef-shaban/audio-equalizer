import altair as alt
import matplotlib.pyplot as plt
import streamlit as st
import scipy

def equalizer(mode, signal, points_per_freq, gainsdb_list):
    equalizer_signal = signal.copy()
    for index, slider in enumerate(mode):
        for Range in slider["range"]:
            if gainsdb_list[index] == None:
                gainsdb_list[index] = 0
            if gainsdb_list[index] != 0:
                signal= equalizer_signal[int(points_per_freq * (Range[0])):int(points_per_freq * Range[1])]
                triangle_window= scipy.signal.windows.triang(len(signal))*10 ** (gainsdb_list[index] / 10)
                equalizer_signal[int(points_per_freq * Range[0]):int(points_per_freq * Range[1])] *= triangle_window
    return equalizer_signal


def initial_time_graph(df1,df2):
    resize = alt.selection_interval(bind='scales')
    chart1 = alt.Chart(df1).mark_line().encode(
    x=alt.X('time:T', axis=alt.Axis(title='date',labels=False)),
    y=alt.Y('signal:Q',axis=alt.Axis(title='value'))
    ).properties(
        width=600,
        height=220
    ).add_selection(
        resize
    )

    chart2 = alt.Chart(df2).mark_line().encode(
        x=alt.X('time:T', axis=alt.Axis(title='date',labels=False)),
        y=alt.Y('signal:Q',axis=alt.Axis(title='value'))
    ).properties(
        width=600,
        height=220
    ).add_selection(
        resize
    )


    chart=alt.concat(chart1, chart2)
    return chart


def plot_animation(df1,df2):
    chart1 = alt.Chart(df1).mark_line().encode(
    x=alt.X('time:T', axis=alt.Axis(title='date',labels=False)),
    y=alt.Y('signal:Q',axis=alt.Axis(title='value'))
    ).properties(
        width=600,
        height=220
    )

    chart2 = alt.Chart(df2).mark_line().encode(
        x=alt.X('time:T', axis=alt.Axis(title='date',labels=False)),
        y=alt.Y('signal:Q',axis=alt.Axis(title='value'))
    ).properties(
        width=600,
        height=220
    )

    chart=alt.concat(chart1, chart2)

    return chart


def plot_spectrogram(fig,ax,signal):
    fig.set_figheight(4)
    fig.set_figwidth(10)
    specto1=ax.specgram(signal,cmap='hsv')
    fig.colorbar(specto1[3], ax=ax)
    return fig
