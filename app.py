import streamlit as st
import streamlit_vertical_slider as svs
from scipy.io.wavfile import read,write
from scipy.fft import rfft, irfft
import numpy as np
import altair as alt
import pandas as pd
import time
from utils import equalizer, mode1

st.set_page_config(
    page_title="Equalizer",
    page_icon="🔊",
    layout="wide"
)
# with open("style.css") as design:
#     st.markdown(f"<style>{design.read()}</style>", unsafe_allow_html=True)
if "is_uploaded" not in st.session_state:
    st.session_state.is_uploaded=True
graph_container= st.container()
returned_signal= np.zeros(1000)

if "time" not in st.session_state:
    st.session_state.time=np.linspace(0,5,1000)

uploader= st.file_uploader("upload wav")

if uploader:
    st.audio(uploader)
    if st.session_state.is_uploaded:
        sample_rate, signal= read(uploader)
        time=signal.shape[0]/sample_rate
        st.session_state["time"]=np.linspace(0,signal.shape[0],signal.shape[0])
        mono= signal.copy()
        st.session_state["sample_rate"]=sample_rate
        st.session_state["transformed_signal"]= rfft(mono)
        st.session_state["points_per_freq"] = len(st.session_state["transformed_signal"]) / (sample_rate / 2)
        st.session_state.is_uploaded=False
    
    gain_list=[]
    for i in range(10):
        try:
            gain_list.append(st.session_state[f"slider{i}"])
        except:
            gain_list.append(0)
    transformed= equalizer(mode1,st.session_state["transformed_signal"],st.session_state["points_per_freq"],gain_list)
    returned_signal= np.asarray(irfft(transformed), dtype=np.int16)
    modified_audio=write("clean.wav",st.session_state["sample_rate"], returned_signal)
else:
    st.session_state.is_uploaded=True
    

cols= st.columns([ 1 for i in range(10)])
for index,i in enumerate(cols):
    with i:
        svs.vertical_slider(key=f"slider{index}",default_value=0.0,min_value=-12.0,max_value=12.0,step=0.1, )
# for i in range(10):
#     st.write(st.session_state[f"slider{i}"])

if uploader:
    st.audio("clean.wav")

ploted_data= pd.DataFrame({"time":st.session_state.time[::300],"signal":returned_signal[::300]})
df=ploted_data.iloc[0:1500]
lines = alt.Chart(df).mark_line().encode(
    x=alt.X('time:T', axis=alt.Axis(title='date',labels=False)),
    y=alt.Y('signal:Q',axis=alt.Axis(title='value')),
    ).properties(
        width=600, 
        height=300
    ).configure_view(strokeWidth=0).configure_axis(grid=False, domain=False)

def plot_animation(df):
    lines = alt.Chart(df).mark_line().encode(
    x=alt.X('time:T', axis=alt.Axis(title='date',labels=False)),
    y=alt.Y('signal:Q',axis=alt.Axis(title='value')),
    ).properties(
        width=600, 
        height=300
    ).configure_view(strokeWidth=0).configure_axis(grid=False, domain=False)
    return lines

N = ploted_data.shape[0] 
burst = 1500       
line_plot= graph_container.altair_chart(lines,use_container_width=True)
start_btn = graph_container.button('Start')

if start_btn:
    for i in range(1500,N-burst):
        step_df = ploted_data.iloc[i:burst+i]       
        lines = plot_animation(step_df)
        line_plot.altair_chart(lines,use_container_width=True)
        
        
# line_plot = st.altair_chart(lines)