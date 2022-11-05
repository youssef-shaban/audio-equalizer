import streamlit.components.v1 as components
import streamlit as st
import os
root_dir= os.path.dirname(os.path.abspath(__file__))
build_dir= os.path.join(root_dir,"frontend","build")
_vertical_slider = components.declare_component(
    "Vertical Silder",
    path=build_dir
)

def VerticalSlider(minValue=0, maxValue=100, step=1,default=0,height=400,label=None,disabled=False,key=None):
    return _vertical_slider(minValue=minValue,maxValue=maxValue,step=step,default=default,height=height,label=label,disabled=disabled,key=key)

