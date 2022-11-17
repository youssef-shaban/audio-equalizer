import streamlit as st
from scipy.io.wavfile import read, write
from scipy.fft import rfft, irfft
from scipy.signal import chirp
import numpy as np
import pandas as pd
from utils import equalizer, initial_time_graph, plot_animation, plot_spectrogram2, create_sliders, VerticalSlider, \
    pitch_shifting, basic_mode
import json
import altair as alt
import matplotlib.pyplot as plt
import streamlit_nested_layout

# App Configurations
st.set_page_config(
    page_title="SigEqualizer",
    page_icon="https://cdn1.iconfinder.com/data/icons/communication-380/64/sound-signal-equalizer-tune-voice-512.png",
    layout="wide"
)


# Adding our Header
header_code = (open("templates/header.html", 'r', encoding='utf-8')).read()
st.markdown(f'{header_code}', unsafe_allow_html=True)

# Adding our Styling
style = (open("static/css/style.css", 'r', encoding='utf-8')).read()
st.markdown(f'{style}', unsafe_allow_html=True)

with open("modes.json") as infile:
    data = json.load(infile)

if "is_uploaded" not in st.session_state:
    st.session_state.is_uploaded = True

if "time" not in st.session_state:
    st.session_state.time = np.linspace(0, 15, 44100 * 30)
if "original_signal" not in st.session_state:
    st.session_state.original_signal = chirp(st.session_state.time, f0=0, f1=20000, t1=15) * 25000
if "sample_rate" not in st.session_state:
    st.session_state.sample_rate = 44100
if "graph_position" not in st.session_state:
    st.session_state.graph_position = 1
if "default_file" not in st.session_state:
    st.session_state.default_file = "sweep.wav"
if "resize" not in st.session_state:
    st.session_state.resize = alt.selection_interval(bind='scales')
returned_signal = chirp(st.session_state["time"], f0=12.5, f1=2.5, t1=10, method='linear')
data["Equalizer"]["sliders"] = basic_mode(st.session_state.sample_rate, data["Equalizer"]["num_sliders"])

left_col, right_col = st.columns([1.3, 4])
with left_col:
    l, r = st.columns([1.5, 1])
    mode = r.selectbox('Modes', data["modes"])
    uploader = l.file_uploader('Upload File')

    col_sub_left_l, col_sub_left_r = st.columns(2)
    col_sub_left_l.write('Graph Control')
    placeholder = col_sub_left_l.empty()
    forward_btn = placeholder.button('Start')
    col_sub_left_r.write('Graph Speed')
    speed_slider = col_sub_left_r.slider('Graph Speed', label_visibility='collapsed', step=1, min_value=1, max_value=5)

if mode == "vowels":
    st.markdown("""
        <style>
        iframe{
            padding-left:5rem;
            }
        </style>
        """, unsafe_allow_html=True)
elif mode == "music":
    st.markdown("""
            <style>
            iframe{
                padding-left:1rem;
                }
            </style>
            """, unsafe_allow_html=True)


bottomCols = [(2 / data[mode]["num_sliders"]) for i in range(data[mode]["num_sliders"])]
bottomCols = st.columns([0.7, *bottomCols])
for index, i in enumerate(bottomCols[1:]):
    with i:
            VerticalSlider(default=data[mode]["sliders"][index]["default"], minValue=data[mode]["sliders"][index]["min_value"], maxValue=data[mode]["sliders"][index]["max_value"], step=0.1, height=200,
                           label=data[mode]["sliders"][index]["label"], key=f"slider{mode}{index}")


if uploader:
    sample_rate, signal = read(uploader)
    with left_col:
        st.write("Original Sound")
        st.audio(uploader)
else:
    sample_rate, signal = read(st.session_state.default_file)
    with left_col:
        st.write("Original Sound")
        st.audio(st.session_state.default_file)

if len(signal.shape) > 1:
    signal = signal[:, 0]
time = signal.shape[0] / sample_rate
st.session_state["time"] = np.linspace(0, signal.shape[0], signal.shape[0])
mono = signal.copy()
st.session_state["sample_rate"] = sample_rate
st.session_state["original_signal"] = mono
st.session_state["transformed_signal"] = rfft(mono)

st.session_state["points_per_freq"] = len(st.session_state["transformed_signal"]) / (sample_rate / 2)
st.session_state.is_uploaded = False

gain_list = []
for i in range(data[mode]["num_sliders"]):
    try:
        gain_list.append(st.session_state[f"slider{mode}{i}"])
    except:
        gain_list.append(0)
if mode == "Pitch Shift":

    returned_signal = pitch_shifting(st.session_state["original_signal"], st.session_state["sample_rate"], gain_list,
                                     np.max(st.session_state["original_signal"]))
else:
    transformed = equalizer(data[mode]["sliders"], st.session_state["transformed_signal"],
                            st.session_state["points_per_freq"], gain_list)
    returned_signal = irfft(transformed)
modified_audio = write("clean.wav", st.session_state["sample_rate"], returned_signal.astype(np.int16))
with left_col:
    st.write("Modified sound")
    st.audio("clean.wav")

if mode == "Pitch Shift":
    changed_time = np.linspace(0, returned_signal.shape[0], returned_signal.shape[0])
    plotted_rec_data = pd.DataFrame({"time": changed_time[::300], "signal": returned_signal[::300]})
else:
    plotted_rec_data = pd.DataFrame({"time": st.session_state.time[::300], "signal": returned_signal[::300]})


def plot_time():
    global plotted_ori_data
    plotted_ori_data = pd.DataFrame(
        {"time": st.session_state.time[::300], "signal": st.session_state["original_signal"][::300]})
    global position
    position = st.session_state["graph_position"]
    global line_plot_rec
    line_plot_rec = st.altair_chart(initial_time_graph(plotted_ori_data, plotted_rec_data, st.session_state.resize))


def plot_spectrogram():
    spectrogram_1, spectrogram_2 = st.columns(2)
    fig1 = plot_spectrogram2(st.session_state["original_signal"])
    spectrogram_1.markdown("<center><strong> Original Spectrogram </strong></center>", unsafe_allow_html=True)
    spectrogram_1.plotly_chart(fig1, use_container_width=True)
    fig2 = plot_spectrogram2(returned_signal)
    spectrogram_2.markdown("<center><strong> Modified Spectrogram </strong></center>", unsafe_allow_html=True)
    spectrogram_2.plotly_chart(fig2, use_container_width=True)


with right_col:
    plot_time()
    show_hist = left_col.checkbox('Show Spectrogram')
    spectrogram_1, spectrogram_2 = st.columns(2)
    if show_hist:
        plot_spectrogram()
    else:
        plt.style.use('ggplot')
        fig1, ax = plt.subplots()
        fig1.set_figheight(4.2)
        fig1.set_figwidth(10)
        spectrogram_1.pyplot(fig1, clear_figure=True)
        fig2, ax = plt.subplots()
        fig2.set_figheight(4.2)
        fig2.set_figwidth(10)
        spectrogram_2.pyplot(fig2, clear_figure=True)

if forward_btn:
    placeholder.empty()
    pause_btn = placeholder.button('Pause')
    N = plotted_rec_data.shape[0]
    burst = int(len(plotted_ori_data) / 4)
    for i in range(st.session_state["graph_position"] + burst, N - burst, speed_slider):
        st.session_state["graph_position"] = i
        step_df_rec = plotted_rec_data.iloc[i:burst + i]
        step_df_ori = plotted_ori_data.iloc[i:burst + i]
        chart = plot_animation(step_df_ori, step_df_rec, st.session_state.resize)
        line_plot_rec.altair_chart(chart, use_container_width=True)
    position = st.session_state["graph_position"]
    line_chart = initial_time_graph(plotted_ori_data, plotted_rec_data, st.session_state.resize)
    line_plot_rec.altair_chart(line_chart)
    st.session_state["graph_position"] = 0

try:
    if pause_btn:
        st.stop()
except:
    pass

