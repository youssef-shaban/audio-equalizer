import altair as alt
import matplotlib.pyplot as plt
import streamlit as st
import scipy
import pandas as pd
from scipy import signal
import numpy as np
import plotly.graph_objects as go

def equalizer(mode, signal, points_per_freq, gainsdb_list):
    equalizer_signal = signal.copy()
    for index, slider in enumerate(mode):
        for Range in slider["range"]:
            if gainsdb_list[index] == None:
                gainsdb_list[index] = 0
            signal= equalizer_signal[int(points_per_freq * (Range[0])):int(points_per_freq * Range[1])]
            triangle_window= scipy.signal.windows.triang(len(signal))
            if gainsdb_list[index]<-10:
                values= 10**((-1000000)*triangle_window)
            else:
                values= 10**((gainsdb_list[index]/10)*triangle_window)
            equalizer_signal[int(points_per_freq * Range[0]):int(points_per_freq * Range[1])] *= values
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
        width=400,
        height=240
    )

    chart2 = alt.Chart(df2).mark_line().encode(
        x=alt.X('time:T', axis=alt.Axis(title='date',labels=False)),
        y=alt.Y('signal:Q',axis=alt.Axis(title='value'))
    ).properties(
        width=400,
        height=240
    )

    chart=alt.concat(chart1, chart2)

    return chart


def plot_spectrogram(fig,ax,signal):
    fig.set_figheight(4)
    fig.set_figwidth(10)
    specto1=ax.specgram(signal)
    fig.colorbar(specto1[3], ax=ax)
    return fig


def plot_spectrogram2(Signal):
    f, t, Sxx=signal.spectrogram(Signal)
    fig=go.Figure(data=go.Heatmap(
                    z=10*np.log10(Sxx), x=f, y=t))
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0),height=250,autosize=False)
    return fig