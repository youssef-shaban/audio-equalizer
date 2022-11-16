import altair as alt
import matplotlib.pyplot as plt
import streamlit as st
import scipy
import pandas as pd
from scipy import signal
import numpy as np
import plotly.graph_objects as go
import streamlit.components.v1 as components
import os
import pyrubberband.pyrb as pyrd

root_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(root_dir, "Vertical_slider", "vertical_slider", "frontend", "build")
_vertical_slider = components.declare_component(
    "Vertical Slider",
    path=build_dir
)


def VerticalSlider(minValue=0, maxValue=100, step=1, default=0, height=400, label=None, disabled=False, key=None):
    return _vertical_slider(minValue=minValue, maxValue=maxValue, step=step, default=default, height=height,
                            label=label, disabled=disabled, key=key)


def equalizer(mode, signal, points_per_freq, gainsdb_list):
    equalizer_signal = signal.copy()
    for index, slider in enumerate(mode):
        for Range in slider["range"]:
            if gainsdb_list[index] == None:
                gainsdb_list[index] = 0
            signal = equalizer_signal[int(points_per_freq * (Range[0])):int(points_per_freq * Range[1])]
            triangle_window = scipy.signal.windows.triang(len(signal))
            if gainsdb_list[index] < -10:
                values = 10 ** ((-1000000) * triangle_window)
            else:
                values = 10 ** ((gainsdb_list[index] / 10) * triangle_window)
            equalizer_signal[int(points_per_freq * Range[0]):int(points_per_freq * Range[1])] *= values
    return equalizer_signal


def basic_mode(sample_rate, num_slider):
    fmax = sample_rate // 2
    lower = 0
    upper = 0
    mode = []
    for i in range(num_slider):
        upper = int(fmax * ((i + 1) / num_slider))
        mean = (upper + lower) // 2
        slider = {
            "label": f"{mean}",
            "range": [[lower, upper]]
        }
        mode.append(slider)
        lower = upper
    return mode


def initial_time_graph(df1, df2, resize):
    chart1 = alt.Chart(df1).mark_line().encode(
        x=alt.X('time:T', axis=alt.Axis(title='time(sec)', labels=False)),
        y=alt.Y('signal:Q', axis=alt.Axis(title='Amplitude'))
    ).properties(
        # width=550,
        height=220,
        title="Original Audio"
    ).add_selection(
        resize
    )

    chart2 = alt.Chart(df2).mark_line().encode(
        x=alt.X('time:T', axis=alt.Axis(title='time(sec)', labels=False)),
        y=alt.Y('signal:Q', axis=alt.Axis(title='Amplitude'))
    ).properties(
        height=220,
        title="Modified Audio",
    ).add_selection(
        resize
    )

    chart = alt.concat(chart1, chart2)
    return chart


def plot_animation(df1, df2, resize):
    chart1 = alt.Chart(df1).mark_line().encode(
        x=alt.X('time:T', axis=alt.Axis(title='time', labels=False)),
        y=alt.Y('signal:Q', axis=alt.Axis(title='Amplitude'))
    ).properties(
        width=550,
        height=230,
        title="Original Audio"
    ).add_selection(
        resize
    )

    chart2 = alt.Chart(df2).mark_line().encode(
        x=alt.X('time:T', axis=alt.Axis(title='time', labels=False)),
        y=alt.Y('signal:Q', axis=alt.Axis(title='Amplitude'))
    ).properties(
        width=550,
        height=230,
        title="Modified Audio"
    ).add_selection(
        resize
    )

    chart = alt.concat(chart1, chart2)

    return chart


def plot_spectrogram2(Signal):
    f, t, Sxx = signal.spectrogram(Signal)
    Sxx = np.round(Sxx, 6)

    fig = go.Figure(data=go.Heatmap(
        z=10 * np.log10(Sxx), x=f, y=t))
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=250, autosize=False,
                      xaxis_title="time(sec)",
                      yaxis_title="frequency(Hz)",
                      )
    return fig


def create_sliders(index):
    if index == 0:
        VerticalSlider(default=0.0, minValue=-5.0, maxValue=5.0, step=0.1, height=200,
                       label="Shift", key=f"sliderPitch Shift0")
    elif index == 1:
        VerticalSlider(default=1.0, minValue=0.3, maxValue=5.0, step=0.1, height=200,
                       label="Stretch", key=f"sliderPitch Shift1")
    st.markdown("""
        <style>
        iframe{{
                padding-left:13rem;
            }}
        </style>
        """, unsafe_allow_html=True)



def pitch_shifting(signal, sampling_rate, gain_list, max_value):
    output = signal.copy()
    if gain_list[0] == None: gain_list[0] = 0
    if gain_list[1] == None: gain_list[1] = 1
    output = pyrd.pitch_shift(output, sampling_rate, gain_list[0])
    output = pyrd.time_stretch(output, sampling_rate, gain_list[1])
    if max(output) < 10:
        output *= max_value
    return output
