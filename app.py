import streamlit as st
from scipy.io.wavfile import read,write
from scipy.fft import rfft, irfft
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
from utils import equalizer,initial_time_graph, plot_animation
import streamlit.components.v1 as components
import os

root_dir= os.path.dirname(os.path.abspath(__file__))
build_dir= os.path.join(root_dir,"Virtical_slider","vertical_slider","frontend","build")
_vertical_slider = components.declare_component(
    "Vertical Silder",
    path=build_dir
)

def VerticalSlider(minValue=0, maxValue=100, step=1,default=0,height=400,label=None,disabled=False,key=None):
    return _vertical_slider(minValue=minValue,maxValue=maxValue,step=step,default=default,height=height,label=label,disabled=disabled,key=key)

st.set_page_config(
    page_title="Equalizer",
    page_icon="🔊",
    layout="wide"
)
with open("modes.json") as infile:
    data = json.load(infile)

if "is_uploaded" not in st.session_state:
    st.session_state.is_uploaded=True

returned_signal= np.zeros(1000)
if "time" not in st.session_state:
    st.session_state.time=np.linspace(0,5,1000)
if "original_signal" not in st.session_state:
    st.session_state.original_signal=np.zeros(1000)
if "sample_rate" not in st.session_state:
    st.session_state.sample_rate=10


col1, col2, col3= st.columns([0.7,1,1])
with col1:
    mode=st.selectbox("Mode",data["modes"])
    uploader= st.file_uploader("upload wav")

col5,col6,col7= st.columns([0.7,1,1])
cols= [ 0.2 for i in range(data[mode]["num_sliders"])]
cols= st.columns([0.7,*cols])
for index,i in enumerate(cols[1:]):
    with i:
        VerticalSlider(default=0.0,minValue=-30.0,maxValue=30.0,step=0.1,height=200,label=data[mode]["sliders"][index]["label"],key=f"slider{index}" )

if uploader:
    
    if st.session_state.is_uploaded:
        sample_rate, signal= read(uploader)
        time=signal.shape[0]/sample_rate
        st.session_state["time"]=np.linspace(0,signal.shape[0],signal.shape[0])
        mono= signal.copy()
        st.session_state["sample_rate"]=sample_rate
        st.session_state["original_signal"]=mono
        st.session_state["transformed_signal"]= rfft(mono)
        st.session_state["points_per_freq"] = len(st.session_state["transformed_signal"]) / (sample_rate / 2)
        st.session_state.is_uploaded=False
    
    gain_list=[]
    for i in range(data[mode]["num_sliders"]):
        try:
            gain_list.append(st.session_state[f"slider{i}"])
        except:
            gain_list.append(0)
    transformed= equalizer(data[mode]["sliders"],st.session_state["transformed_signal"],st.session_state["points_per_freq"],gain_list)
    returned_signal= np.asarray(irfft(transformed), dtype=np.int16)
    modified_audio=write("clean.wav",st.session_state["sample_rate"], returned_signal)
else:
    st.session_state.is_uploaded=True
    st.session_state.time=np.linspace(0,5,1000)
    


if uploader:
    with col5:
        st.write("Original Sound")
        st.audio(uploader)
        st.write("Modified sound")
        st.audio("clean.wav")

ploted_rec_data= pd.DataFrame({"time":st.session_state.time[::300],"signal":returned_signal[::300]})
ploted_ori_data= pd.DataFrame({"time":st.session_state.time[::300],"signal":st.session_state["original_signal"][::300]})
lines_rec = initial_time_graph(ploted_rec_data.iloc[0:700])
lines_ori = initial_time_graph(ploted_ori_data.iloc[0:700])



N = ploted_rec_data.shape[0] 
burst = 700       
line_plot_rec= col2.altair_chart(lines_rec,use_container_width=True)
line_plot_ori= col3.altair_chart(lines_ori,use_container_width=True)
fig,ax= plt.subplots()
fig.set_figheight(4)
fig.set_figwidth(10)
ax.specgram(st.session_state["original_signal"],Fs=st.session_state["sample_rate"])
col6.pyplot(fig,clear_figure=True)
fig,ax= plt.subplots()
fig.set_figheight(4)
fig.set_figwidth(10)
ax.specgram(returned_signal,Fs=st.session_state["sample_rate"])
col7.pyplot(fig,clear_figure=True)
start_btn = col7.button('Start')
if start_btn:
    for i in range(burst,N-burst):
        step_df_rec = ploted_rec_data.iloc[i:burst+i]       
        step_df_ori = ploted_ori_data.iloc[i:burst+i]       
        lines_rec = plot_animation(step_df_rec)
        lines_ori = plot_animation(step_df_ori)
        line_plot_rec.altair_chart(lines_rec,use_container_width=True)
        line_plot_ori.altair_chart(lines_ori,use_container_width=True)
        
        
