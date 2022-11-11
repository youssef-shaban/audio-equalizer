import streamlit as st
from scipy.io.wavfile import read, write
from scipy.fft import rfft, irfft
from scipy.signal import chirp
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from utils import equalizer, initial_time_graph, plot_animation,plot_spectrogram2
import streamlit.components.v1 as components
import json
import os
import altair as alt


root_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(root_dir, "Vertical_slider", "vertical_slider", "frontend", "build")
_vertical_slider = components.declare_component(
    "Vertical Slider",
    path=build_dir
)


def VerticalSlider(minValue=0, maxValue=100, step=1, default=0, height=400, label=None, disabled=False, key=None):
    return _vertical_slider(minValue=minValue, maxValue=maxValue, step=step, default=default, height=height,
                            label=label, disabled=disabled, key=key)


st.set_page_config(
    page_title="Equalizer",
    page_icon="🔊",
    layout="wide"
)
with open("modes.json") as infile:
    data = json.load(infile)


if "is_uploaded" not in st.session_state:
    st.session_state.is_uploaded = True


if "time" not in st.session_state:
    st.session_state.time = np.linspace(0, 15, 44100*30)
if "original_signal" not in st.session_state:
    st.session_state.original_signal = chirp(st.session_state.time, f0=0, f1=20000, t1=15)*25000
if "sample_rate" not in st.session_state:
    st.session_state.sample_rate = 44100
if "graph_position" not in st.session_state:
    st.session_state.graph_position = 1
if "default_file" not in st.session_state:
    st.session_state.default_file="sweep.wav"
if "resize" not in st.session_state:
    st.session_state.resize=alt.selection_interval(bind='scales')
returned_signal = chirp(st.session_state["time"], f0=12.5, f1=2.5, t1=10, method='linear')

topCol1, topCol2= st.columns([0.7, 2])
with topCol1:
    mode = st.selectbox("Mode", data["modes"])
    uploader = st.file_uploader("upload wav")
    

midCol1, midCol2, midCol3 = st.columns([0.7, 1, 1])
bottomCols = [0.2 for i in range(data[mode]["num_sliders"])]
bottomCols = st.columns([0.7, *bottomCols])
for index, i in enumerate(bottomCols[1:]):
    with i:
        VerticalSlider(default=0.0, minValue=-15.0, maxValue=15.0, step=0.1, height=200,
                       label=data[mode]["sliders"][index]["label"], key=f"slider{mode}{index}")

if uploader:
    sample_rate, signal = read(uploader)
    with bottomCols[0]:
        st.write("Original Sound")
        st.audio(uploader)
else:
    sample_rate, signal = read(st.session_state.default_file)
    with bottomCols[0]:
        st.write("Original Sound")
        st.audio(st.session_state.default_file)

if len(signal.shape)>1:
    signal=signal[:,0]
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
transformed = equalizer(data[mode]["sliders"], st.session_state["transformed_signal"],
                        st.session_state["points_per_freq"], gain_list)
returned_signal = irfft(transformed)
modified_audio = write("clean.wav", st.session_state["sample_rate"],returned_signal.astype(np.int16))
with bottomCols[0]:
    st.write("Modified sound")
    st.audio("clean.wav")

ploted_rec_data = pd.DataFrame({"time": st.session_state.time[::300], "signal": returned_signal[::300]})
ploted_ori_data = pd.DataFrame(
    {"time": st.session_state.time[::300], "signal": st.session_state["original_signal"][::300]})
position=st.session_state["graph_position"]
line_chart = initial_time_graph(ploted_ori_data,ploted_rec_data,st.session_state.resize)
line_plot_rec = topCol2.altair_chart(line_chart, use_container_width=True)

show_spec=midCol1.checkbox("generate Spectogram")
if show_spec:
    fig1=plot_spectrogram2(st.session_state["original_signal"])
    midCol2.plotly_chart(fig1, use_container_width=True)
    fig2=plot_spectrogram2(returned_signal)
    midCol3.plotly_chart(fig2, use_container_width=True)
else:
    fig1, ax = plt.subplots()
    fig1.set_figheight(4)
    fig1.set_figwidth(10)
    midCol2.pyplot(fig1, clear_figure=True)
    fig2, ax = plt.subplots()
    fig2.set_figheight(4)
    fig2.set_figwidth(10)
    midCol3.pyplot(fig2, clear_figure=True)


forward_btn = midCol1.button('Forward')
stop_btn = midCol1.button('stop')
pause_btn = midCol1.button('Pause')
speed_slider= midCol1.slider(label="Graph Speed",step=1,min_value=1,max_value=5)
if forward_btn:
    N = ploted_rec_data.shape[0]
    burst = int(len(ploted_ori_data)/4)
    for i in range(st.session_state["graph_position"]+burst, N - burst,speed_slider):
        st.session_state["graph_position"]=i
        step_df_rec = ploted_rec_data.iloc[i:burst + i]
        step_df_ori = ploted_ori_data.iloc[i:burst + i]
        chart= plot_animation(step_df_ori,step_df_rec,st.session_state.resize)
        line_plot_rec.altair_chart(chart, use_container_width=True)
    position=st.session_state["graph_position"]
    line_chart = initial_time_graph(ploted_ori_data,ploted_rec_data,st.session_state.resize)
    line_plot_rec.altair_chart(line_chart)
    st.session_state["graph_position"]=0

if stop_btn:
    st.session_state["graph_position"]=0
    st.stop()
if pause_btn:
    st.stop()


