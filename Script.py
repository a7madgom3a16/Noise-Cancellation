# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#Importing the needed libraries
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import math
from scipy.fftpack import fft

#Defining the frequencies of notes to be used in the 4th octave & depending on
#the fact that the frequency of the same note in the 3rd octave is half of it
C = 261.63
D = 293.66
E = 329.63
F = 349.23
G = 392
A = 440
B = 493.88

#Creating 12*1024 samples for 3 seconds
t = np.linspace(0, 3, 12*1024)

#Creating a list of notes to be played
n = [F, D, D, E, F, E, D, C, D, E, B, F, B, C, D, E, D, C, A, G]

#Duration of each note
d = 0.1

#Total signal
s = 0

#Starting time of each note, gets updated in the loop to achieve different
#starting times for each note
p = 0

#Creating a loop to play each note from the array sequentially in the 3rd &
#4th octaves together
for x in n:
    s += ((np.sin(2*np.pi*x*t)) + (np.sin(np.pi*x*t))) * ((t>=p) & (t<=p+d))
    p += d+0.053

#Plotting the total signal over the time domain
plt.subplot(3,2,1)
plt.plot(t, s)

#Playing the audio
#sd.play(s, 3*1024)

#Setting the number of samples
N = 3*1024

#Setting the frequency axis range
f = np.linspace(0, 512, int(N/2))

#Getting the Fourier transform of the original signal and plotting it
sf = fft(s)
sf = 2/N * np.abs(sf[0:np.int(N/2)])
plt.subplot(3,2,2)
plt.plot(f, sf)

#Getting the peak of the original signal in Fourier transform and rounding it
#up
m=math.ceil(np.amax(sf))

#Generating 2 random frequencies as the noise, adding them to the original
#signal and plotting the result
fn1, fn2 = np.random.randint(0, 512, 2)
n = (np.sin(2*np.pi*fn1*t)) + (np.sin(2*np.pi*fn2*t))
sn = s+n
plt.subplot(3,2,3)
plt.plot(t, sn)

#Getting the Fourier transform of the resultant signal and plotting it
snf = fft(sn)
snf = 2/N * np.abs(snf[0:np.int(N/2)])
plt.subplot(3,2,4)
plt.plot(f, snf)

#Putting the y-values of the resultant signal in Fourier transform in an array
e = []
for i in snf:
    e.append(i)

#Putting the frequencies at which these y-values are higher than the peak of
#the original signal in Fourier transform in an array
l = []
for y in e :
    if y>m :
        l.append(round(f[e.index(y)]))

#Creating the final signal by subtracting the noise created by the 2 random
#frequencies from the signal containing the noise and plotting it
sx = sn - ((np.sin(2*np.pi*l[0]*t)) + (np.sin(2*np.pi*l[1]*t)))
plt.subplot(3,2,5)
plt.plot(t, sx)

#Getting the Fourier transform of the final signal and plotting it
sxf = fft(sx)
sxf = 2/N * np.abs(sxf[0:np.int(N/2)])
plt.subplot(3,2,6)
plt.plot(f, sxf)

#Playing the audio after noise cancellation
sd.play(sx, 3*1024)
