import os
import time

import pygame
from gtts import gTTS
import asyncio



def read_aloud(input_text):
    """[summary]
    Generates a sound file from input text
    
    Arguments:
        input_text {[string]} -- [text to be read aloud]
    """
    tts = gTTS(text=input_text, lang='en-au', slow=False)
    title = 'story.mp3'
    tts.save(title)


async def foo(file_name):
    if file_name:
        await start_player(file_name)

def start_player(file_name):
    """[summary]
    Plays audio file using pygame mixer
    
    Arguments:
        file_name {[.mp3]} -- [file to be played]
    """
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(file_name)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)
    except Exception as message:
        print(message)
    pygame.mixer.quit()

#sample_text = "wake up"
#read_aloud(sample_text)
