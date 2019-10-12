# import win32com.client as wincl

# import pyTTS

# speak = wincl.Dispatch("SAPI.SpVoice")
# speak.Speak("Fuck you your origami sucks")

import pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 300)   
voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
# engine.setProperty('voice', voices[1].id)   #  # setting up new voice rate
engine.say("I will speak this text")
rate = engine.getProperty('rate')   # getting details of current speaking rate

engine.say('My current speaking rate is ' + str(rate))
strin = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc finibus interdum quam. Mauris venenatis justo nunc, nec pretium enim scelerisque sed. In vitae ullamcorper nunc. Quisque dignissim tempor lacus, maximus vulputate ante ultricies in. Nunc vulputate in velit quis pharetra. Praesent vel nunc nibh. Donec eget odio et odio fringilla suscipit eget et leo. Pellentesque elementum commodo tellus at congue. Vivamus in lacus laoreet, facilisis tellus non, porttitor enim. Nullam maximus mauris non urna tincidunt tincidunt."
engine.say(strin)

engine.runAndWait()