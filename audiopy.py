import os
import time

import pygame
from gtts import gTTS


def read_aloud(input_text):
    tts = gTTS(text=input_text, lang='en-au', slow=False)
    title = 'story.mp3'
    tts.save(title)
    start_player(title)

def start_player(file_name):
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(file_name)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)
    except pygame.error as message:
        print(message)
    pygame.mixer.quit()
    os.remove('story.mp3')

sample_text = "Hello, my name is Bob"
read_aloud(sample_text)
