# Alics （this is a gpt aided project)
Here is the youtube mockup video. 
https://www.youtube.com/watch?v=NeDrukDnJQE

# I recommand you to run this program in ANACONDA enviroment
https://www.anaconda.com/download

to use this chatbot 

You will need to download the following package 


## Download python 3.9 or 3.10 ( because we use oepn ai whisper for speech rec, we are going to need numba, but numba does not run on 3.11 python, so DONT DOWNLOAD PYTHON 3.11, go with 3.9 in anaconda.

https://www.python.org/downloads/release/python-3916/

Open Ai whisper
https://github.com/openai/whisper
```
pip install -U openai-whisper
```
python speech rec
https://pypi.org/project/SpeechRecognition/
```
pip install SpeechRecognition
```
11 labs python library
https://github.com/elevenlabs/elevenlabs-python
```
pip install elevenlabs
```
python simpleaudio
https://pypi.org/project/simpleaudio/
```
pip install simpleaudio
```
python pyaudio (this one might be tricky, if you encounter problem, watch this video https://www.youtube.com/watch?v=gVZZzb_FIXo)
https://pypi.org/project/PyAudio/ 
```
pip install PyAudio   
```
python pydub
https://pypi.org/project/pydub/
// Please install pyaudio before pydub
```
pip install pydub
```
python opencv
https://pypi.org/project/opencv-python/
```
pip install opencv-python
```

## And have the Open ai API, and 11 lab API.
### eleven lab API
https://beta.elevenlabs.io/
### Open ai API
https://openai.com/blog/openai-api

put your api keys and voice ids here
#### in the main.py
```
openai.api_key = f"[YOUR API KEY]]"
API_KEY = f"[YOUR API KEY]]]"
VOICE_ID = "[YOUR VOICE ID]"
```
#### in the clone.py
```
set_api_key(f"[YOUR API KEY]]")
openai.api_key = "[YOUR API KEY]]"
```

# To run the script cd into the main folder and type in the terminal

```
python3 main.py
```
### if you want to run the script with your clone voice type 
```
python3 clone.py
```

# Animation is not included in this repository, you will need to downlaod from my youtube channel

In terms of the animation, I could not uplaod the original animation here, becasue the file size was too big. you could downlaod my animation from youtube.
Remember to create a folder call Alics-vid or any else name you like, and put the video in there. Remember to change the video path in the code. 


## speak animation
https://www.youtube.com/watch?v=P2nngg1idFM

## defult animation
https://www.youtube.com/watch?v=BokfWDG4k-w

### remember to change the video file path here
```
    video_file1 = "/Users//Desktop/interface/Alics_vid/Defult2.MOV"
    video_file2 = "/Users//Desktop/interface/Alics_vid/SPeak.MOV"
```

# To clone your own voice, remember to create a voice_train folder and put as many one miniute recording of yourslef talking as possible in there. And in the clone.py remember to change your file path here

```
def clone_voice():
    voice = clone(
        name="your name",
        description="description of your voice",
        files=["Your file path"],
    )
    return voice
```


