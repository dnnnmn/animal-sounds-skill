import pathlib
import random
import os
from os.path import dirname, exists, join

from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler, intent_file_handler
from mycroft.audio import wait_while_speaking, is_speaking
from mycroft.util import play_wav
from mycroft.skills.audioservice import AudioService


class AnimalSounds(MycroftSkill):
    def __init__(self):
        super(AnimalSounds, self).__init__(name="AnimalSounds")
        self.process = None        
    def initialize(self):
        self.audioservice = AudioService(self.bus)

    @intent_file_handler('sounds.animal.intent')
    def handle_sounds_animal(self, message):
       UnknownAnimal = ["I don't know that animal", "I can't make that sound", "Please give me an easier animal", "You tell me"]                   
       
       animals = [('baby','wha wha'),('bird','tweet tweet'),('cat','meow'),('cow','mooo'),
                   ('dog','woof woof'),('duck','qwack qwack'),('frog','ribbit'),        
                   ('hen','cluck cluck cluck'),('horse','neigh'),('lamb','baa baaa'),
                   ('lion','roar'),('owl','who who'),
                   ('rooster','cock a doodle do'),('wolf','howl')]
       
       synonyms = [('baby','child'),
                    ('bird','gull'),
                    ('cat','kitten'),
                    ('cow','calf'),
                    ('dog','puppy'),('dog','tashie'),
                    ('duck','duck'),
                    ('frog','toad'),        
                    ('hen','chicken'),
                    ('horse','pony'),
                    ('lamb','sheep'),('lamb','goat'),
                    ('lion','lion'),
                    ('owl','owl'),
                    ('rooster','rooster'),
                    ('wolf','coyote')]

       animal_chosen = message.data.get('animal')
       AnimalVoice = animal_chosen
       if animal_chosen != "":
           RndmNum = random.randint(0,4)
           #RndmNum = 0 #causes a speak.dialog rather than recording
           
           #check for synonyms
           for voice, choice in synonyms:
               if (choice == animal_chosen):
                   AnimalVoice = voice
                   break
                
           self.log.debug('animal_chosen is ' + animal_chosen) 
           self.log.debug('AnimalVoice is ' + AnimalVoice)
           self.log.debug('RndmNum is ' + str(RndmNum))         

           # Test to see if animal is defined
           found = False
           for animal, sound in animals:
              if (animal == AnimalVoice):
                  SoundToSpeak = sound
                  found = True
                  break
                
           if found == False: #animal not found
                if RndmNum == 4: #play jeopardy song
                   path =(join(dirname(__file__), "Sounds", "JeopardySongShort.mp3"))
                   if pathlib.Path(path).exists ():
                        self.audioservice.play(path)
                   else: 
                        self.log.error('Path = ' + path)                                                 
                        self.speak_dialog("I seem to be lost. check the error log")                
                else: #say something witty
                    self.speak_dialog(UnknownAnimal[RndmNum])
                    
           else: #The animal is defined
               if (RndmNum == 0): #speak animal sound
                   self.speak_dialog(animal_chosen + ' says ')
                   wait_while_speaking()
                   self.speak_dialog(SoundToSpeak)
               else: #play recording of animal sound                 
                   RndmSnd = AnimalVoice + str(RndmNum) + '.mp3'
                   path = join(dirname(__file__), "Sounds", RndmSnd)    
                   if pathlib.Path(path).exists ():
                        self.speak_dialog(animal_chosen + ' says ')
                        wait_while_speaking()
                        self.audioservice.play(path)                      
                   else: #path not found
                        self.log.error('Path = ' + path)                 
                        self.speak_dialog("I seem to be lost. check the error log")            
       else:
            self.speak_dialog("no animal specified")
            
    def stop(self):
        if self.process and self.process.poll() is None:
            self.speak_dialog('singing.stop')
            self.process.terminate()
            self.process.wait()

def create_skill():
    return AnimalSounds()

