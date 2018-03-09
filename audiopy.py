import os
import time

import pygame
from gtts import gTTS
import asyncio



def read_aloud(input_text):
    tts = gTTS(text=input_text, lang='en-au', slow=False)
    title = 'story.mp3'
    tts.save(title)
    start_player(title)

async def foo(file_name):
    if file_name:
        await start_player(file_name)

async def start_player(file_name):
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(file_name)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(1)
    except pygame.error as message:
        print(message)
    pygame.mixer.quit()

#sample_text = "wake up"
#read_aloud(sample_text)
