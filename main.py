import cv2
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import threading
import openai
import asyncio
import whisper
import speech_recognition as sr
import simpleaudio as sa
from pydub import AudioSegment
import warnings
from numba import NumbaDeprecationWarning
import queue
from elevenlabs import generate, play



warnings.filterwarnings("ignore", category=NumbaDeprecationWarning)

openai.api_key = f"[YOUR API KEY]]"



recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
GPT_WAKE_WORD = "hi alex"
GPT_SLEEP_WORD = "goodbye"
is_audio_playing = False
video_file1 = "/Users/giaogiaoguo/Desktop/interface/Alics_vid/Defult2.MOV"
video_file2 = "/Users/giaogiaoguo/Desktop/interface/Alics_vid/SPeak.MOV"
video_capture1 = cv2.VideoCapture(video_file1)
video_capture2 = cv2.VideoCapture(video_file2)

def create_settings_window(settings):
    settings_window = Tk()
    settings_window.title("ALICS Settings")

    def save_settings():
        settings['system_message'] = system_message_entry.get()
        settings['max_tokens'] = int(max_tokens_entry.get())
        settings_window.destroy()
        settings['settings_open'] = False


    system_message_label = tk.Label(settings_window, text="System message:")
    system_message_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
    system_message_entry = tk.Entry(settings_window)
    system_message_entry.insert(0, settings['system_message'])
    system_message_entry.grid(row=0, column=1, padx=5, pady=5)


    max_tokens_label = tk.Label(settings_window, text="Max tokens:")
    max_tokens_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
    max_tokens_entry = tk.Entry(settings_window)
    max_tokens_entry.insert(0, settings['max_tokens'])
    max_tokens_entry.grid(row=1, column=1, padx=5, pady=5)

 
    save_button = tk.Button(settings_window, text="Save", command=save_settings)
    save_button.grid(row=2, column=1, padx=5, pady=5, sticky="e")

    settings_window.mainloop()

def show_settings_window(settings):
    print("show_settings_window called")
    if not settings['settings_open']:
        settings['settings_open'] = True
        create_settings_window(settings)

def get_wake_word(phrase):
    
   if GPT_WAKE_WORD in phrase.lower():
       return GPT_WAKE_WORD
   else:
       return None
  


def get_sleep_word(phrase):
   if GPT_SLEEP_WORD in phrase.lower():
       return GPT_SLEEP_WORD
   else:
       return None   



API_KEY = f"[YOUR API KEY]]]"
VOICE_ID = "[YOUR VOICE ID]"


def synthesize_speech(text, output_filename):
     audio = generate(text, voice=VOICE_ID, api_key=API_KEY)
     with open(output_filename, 'wb') as f:
         f.write(audio)




def transcribe_audio_with_whisper(audio_file_path):
    model = whisper.load_model("base")  
    result = model.transcribe(audio_file_path)
    return result["text"].strip()

  
def play_audio(file):
    global is_audio_playing
    is_audio_playing = True
    sound = AudioSegment.from_mp3(file) #
    audio_data = sound.export(format="wav")
    audio_data = audio_data.read()

    
    audio_data = audio_data[44:]

    audio_wave = sa.WaveObject(audio_data, sound.channels, sound.sample_width, sound.frame_rate)
    play_obj = audio_wave.play()
    play_obj.wait_done()
    is_audio_playing = False


def process_user_input(user_input, response_queue):
    bot_response = "You said: " + user_input
    response_queue.put(bot_response)





async def main_with_gui(response_queue, text_var, settings):
    wake_word_detected = False
    greeting_played = False

    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)

            if not wake_word_detected:
                print(f"Say {GPT_WAKE_WORD} to start a conversation...")

                while True:
                    audio = recognizer.listen(source)
                    audio_file = "audio.wav"
                    with open(audio_file, "wb") as f:
                        f.write(audio.get_wav_data())

                    phrase = transcribe_audio_with_whisper(audio_file)
                    print(f"Phrase: {phrase}")

                    if get_wake_word(phrase) is not None:
                        wake_word_detected = True
                        break
                    else:
                        print("Not a wake word. Try again.")

            if not greeting_played:
      
                play_audio('greetings.mp3')
                greeting_played = True

            while wake_word_detected:
                print("Speak a prompt...")
                audio = recognizer.listen(source)
                audio_file = "audio_prompt.wav"
                with open(audio_file, "wb") as f:
                    f.write(audio.get_wav_data())

                user_input = transcribe_audio_with_whisper(audio_file)

                print(f"User input: {user_input}")

                if get_sleep_word(user_input) is not None:
                    wake_word_detected = False
                    greeting_played = False
                    print("Sleep word detected, going back to listening for wake word.")

                  
                    play_audio('sleep.mp3')

                 
                    text_var.set("")

                    break

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": settings['system_message']},
                        {"role": "user", "content": user_input},
                    ],
                    temperature=0.6,
                    max_tokens=settings['max_tokens'],
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                    n=1,
                    stop=["\nUser:"],
                )



                bot_response = response["choices"][0]["message"]["content"]

   
                response_queue.put(bot_response)

            
                synthesize_speech(bot_response, 'response.mp3')

      
                play_audio('response.mp3')
                

def create_gui():
    root = Tk()
    root.title("ALICS (Artificial Intelligence for Life Improvement and Counseling Support)")
    menu_bar= tk.Menu(root)
    root.config(menu=menu_bar)
    settings_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Settings", menu=settings_menu)
    settings_menu.add_command(label="Open Settings", command=lambda: show_settings_window(settings))
    settings = {
        'system_message': "Your name is Alice, an acronym for Artistic Intelligence for Life Improvement and Counseling Support. As a creative and insightful personal therapist, your mission is to help clients address their problems with touch of humor. Make an effort to connect with clients on a personal level by sharing relevant anecdotes or insightful metaphors when appropriate.",
        'max_tokens': 150,
        'settings_open': False
    }
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")
    root.configure(bg="black")

    system_message_var = StringVar()
    system_message_var.set(settings['system_message'])
    
    max_tokens_var = IntVar()
    max_tokens_var.set(150)

   
    video_frame = Frame(root, bg="black")
    video_frame.pack(side="top", pady=(10, 0), anchor="center", expand=True)


    video_file1 = "/Users/giaogiaoguo/Desktop/interface/Alics_vid/Defult2.MOV"
    video_file2 = "/Users/giaogiaoguo/Desktop/interface/Alics_vid/SPeak.MOV"

  
    video_capture1 = cv2.VideoCapture(video_file1)
    video_capture2 = cv2.VideoCapture(video_file2)

    
    second_video_frame_rate = 60 
    video_capture2.set(cv2.CAP_PROP_FPS, second_video_frame_rate)


    def update_video_label():
        global is_audio_playing, video_capture1, video_capture2

        if is_audio_playing:
            video_capture = video_capture2
            scale_percent = 30
            frame_rate=100
        else:
            video_capture = video_capture1
            scale_percent = 30  
            frame_rate=100
        ret, frame = video_capture.read()
        if not ret:
            video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = video_capture.read()

        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        width = int(cv2image.shape[1] * scale_percent / 100)
        height = int(cv2image.shape[0] * scale_percent / 100)

        dim = (width, height)
        resized = cv2.resize(cv2image, dim, interpolation=cv2.INTER_AREA)

        img = Image.fromarray(resized)
        imgtk = ImageTk.PhotoImage(image=img)
        label.config(image=imgtk)
        label.imgtk = imgtk
        
        delay= int(1000 / frame_rate)
        root.after(delay, update_video_label)

    
    label = Label(video_frame, bg="black")
    label.pack(side="top", anchor="center")

    update_video_label()

    
    text_frame = Frame(root, bg="black")
    text_frame.pack(side="top", pady=(50, 20), anchor="center", expand=True)

    text_var = StringVar()
    text_widget = tk.Label(text_frame, textvariable=text_var, wraplength=1000, bg="black", fg="white", font=("Nanum Gothic", 12))
    text_widget.pack(expand=True, fill=BOTH, anchor="center")


    response_queue = queue.Queue()
    threading.Thread(target=lambda: asyncio.run(main_with_gui(response_queue, text_var, settings)), daemon=True).start()

    threading.Thread(target=update_text_widget, args=(text_widget, text_var, response_queue, root), daemon=True).start()

    root.mainloop()


def update_text_widget(text_widget, text_var, response_queue, root):
    while True:
        response = response_queue.get()
        text_var.set(f"ALICS: {response}\n")  

if __name__ == "__main__":
   create_gui()













