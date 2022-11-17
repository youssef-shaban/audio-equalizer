# SigEqualizer

## Table of contents:
- [Introduction](#introduction)
- [Project Features](#project-features)
- [Project Structure](#project-structure)
- [How to Run The Project](#run-the-project)
- [Team]()


### Introduction
Signal Equalizers are widely used in different fields to make 
audio processing in music production. By them, you can adjust the volume level of a frequency (or range of frequencies) within a sound, which in turn allows you to cure a sound – or sometimes even entire songs – of its imperfections.
We expanded our Signal Equalizer applications in different domains which are:
- General Audio Processing
  - Music Production
  - Vowels Removal
  - Pitch Shifting and Stretching   
### Project Features
In this web application you can
> 1. Audio Processing on a default mono WAV file

> 2. Upload signals from your computer as mono WAV file format

> 3. Plot the signal in Time Domain as Time Graph where you can play/pause it

> 4. Plot the signal in Frequency Domain as Spectrogram Graph where you can show/hide it

> 5. Switch to general equalizier mode  

> 6. Switch to music mode where you can remove audio instruments from the audio

> 7. Switch to vowels mode where you can remove phonetics from the audio

> 8. Switch to pitch shifting mode where you can change the audio speed and change the audio pitch


### Project Structure
The Web Application is built using:
- Frontend:
  - HTML
  - CSS
- Backend framework:
  - Streamlit (Python)

### Run the Project 
1. Install Python3 in your computer
``` 
Download it from www.python.org/downloads/
```
2. Install the following packages
   - numpy
   - streamlit
   - matplotlib
   - pandas
   - json
   - altair
   - scipy
   - plotly
   - rubberband (you will need to configure its `.exe` path to your system variables to make it work)
 - Open Project Terminal & Run
```
pip install -r requirments.txt
```
3. Start Server by Running 
```
python app.py
```

4. Visit http://127.0.0.1:5000

### Team
First Semester - Biomedical Digital Signal Processing (SBE3110) class project created by:

| Team Members' Names                                   | Section | B.N. |
|-------------------------------------------------------|:-------:|:----:|
| [Mahmoud Salman](https://github.com/mahmoud1yaser)  |    2    |  30   |
| [Maye Khaled](https://github.com/mayekhaled0)         |    2    |  40  |
| [Youssef Shaaban](https://github.com/youssef-shaban)  |    2    |   -  |
| [Abdelrahman Saeed](https://github.com/Abdelrahman-Yousef)       |    1    |  -  |

### Submitted to:
- Dr. Tamer Basha & Eng. Mohamed Mostafa
All rights reserved © 2022 to Team 2 - Systems & Biomedical Engineering, Cairo University (Class 2024)