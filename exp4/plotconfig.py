'''
authour: Mayur Kamat
affiliation: 201104032, TE-E&TC Engg. Sem V, 2021-22, GEC
last updated: 30/10/2022
'''

#importing necessary functions from libraries
from numpy import cos, arange, linspace, fft, abs, argsort, ones
from math import pi

#these are sampling values
fs = 200000
dt= 1/fs
duration = 1
N = duration * fs

#generating time axis samples
time = linspace(0, duration, N)

#carrier signal parameters 
carrierAmp = 10
carrierFreq = 4000

#message signal parameteres
amp = 3
freq = 200

#sensitivity
kf = 200

# Bandwidth threshold, ignores sidebands below this value
BWThreshold = 0.1

#FM moudlation index and BW
#needs to be calculated in the main file
mf = 0
BW = 0

#message and carrier singal variables need to be calculated in the main file
Vm = 0
Vc = 0

#modulated signal variables need to be calculated in main file
Vfm = 0

#spectrum variable needs to be calculated in the main file
spectrum = 0

#generating frequency axis samples
frequency = fft.fftfreq(N, dt)

#sorting frequency axis indices for plotting purpose
idx = argsort(frequency)
frequency_plt = frequency[idx]
