import os
from os.path import dirname, exists

from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler, intent_file_handler
from mycroft.audio import wait_while_speaking, is_speaking
from mycroft.util import play_wav

path = "/home/pi/DBN/BigDog.wav"


class AnimalSounds(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
       self.settings["file_path"] = "/home/pi/DBN/BigDog.wav"

    @intent_file_handler('sounds.animal.intent')
    def handle_sounds_animal(self, message):
        if exists(path):
        #if (1 == 1):

             # Playback the recording
            #play_wav("/home/pi/DBN/BigDog.wav")
            play_wav(path)
 
        else:
           play_wav("/home/pi/DBN/error.wav")
           #self.speak_dialog("file does not exist")


def create_skill():
    return AnimalSounds()

