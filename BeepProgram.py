#Beep Program
from __future__ import division
import random
import math
from pyaudio import PyAudio # sudo apt-get install python{,3}-pyaudio
import pyglet

try:
    from itertools import izip
except ImportError: # Pytho 3
    izip = zip
    xrange = range

def exit_callback(dt):
    pyglet.app.exit()

pyglet.clock.schedule_once(exit_callback , 1000)
player = pyglet.media.Player()


norm_tone = pyglet.media.load('500.wav',streaming=False)
oddball = pyglet.media.load('1000.wav',streaming=False)
#Baseline is 500 Hz and Oddball is 1000 Hz.
#Duration is the number of milliseconds that the sound is played.
Baseline = 500
Oddball = 1000
Duration = 1

#a is 200 numbers starting from 6 (starting from 6 because we don't
#want the first 5 beeps to be oddball). 
#z gives you 40 random numbers from the range of 200 numbers (these are the list of numbers where oddball beep occurs).
#numOddballBeeps is greater than the total number of oddball beeps we want to hear
#because we want a large range of numbers in case the oddball beep gets skipped.
numOddballBeeps = 40
a = range(6, 200)
z = random.sample(a, numOddballBeeps)
print(z)

numBeeps = 300
maxOddballBeeps = 0
normalBeeps = 0
counter = 0
oddballCounter = 0
oddballPlayed = 0
norm_tone.play()
while counter in range(numBeeps):
    if counter not in list(z):
        print "print whatever"
        pyglet.clock.schedule_once(exit_callback , 1)
        norm_tone.play()
        pyglet.app.run()
        print "cry"

        normalBeeps += 1
        oddballPlayed = 0
    else:
        if(oddballPlayed == 0 and maxOddballBeeps < 24):
            pyglet.clock.schedule_once(exit_callback , 1)
            oddball.play()
            pyglet.app.run()
            print "oddball played"
            maxOddballBeeps += 1
            oddballPlayed = 1
            print(counter)
        else:                       #Makes sure that consecutive beeps aren't played.
            pyglet.clock.schedule_once(exit_callback , 1)
            norm_tone.play()
            pyglet.app.run()
            print("odd ball skipped") 
    counter +=1
    if (normalBeeps + maxOddballBeeps >= 200):
        break
    
print(maxOddballBeeps)
print(normalBeeps)
