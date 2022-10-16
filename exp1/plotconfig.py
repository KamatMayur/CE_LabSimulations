'''
authour: Mayur Kamat
affiliation: 201104032, TE-E&TC Engg. Sem V, 2021-22, GEC
last updated: 15/10/2022
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

#filter parameters 
BW = 1300

#carrier signal parameters 
carrierAmp = 10
carrierFreq = 8000

#message signal parameteres
ma1 = 0.6
ma2 = 0.4
m1freq = 200
m2freq = 600

#message and carrier singal variables need to be calculated in the main file
Vm1 = 0
Vm2 = 0
Vc = 0
Vm = 0

#modulated signal variables need to be calculated in main file
Vam = 0
Vdsbsc = 0

#spectrum variable needs to be calculated in the main file
spectrum = 0

#generating frequency axis samples
frequency = fft.fftfreq(N, dt)

#sorting frequency axis indices for plotting purpose
idx = argsort(frequency)
frequency_plt = frequency[idx]

#demodulated signal, demodulated spectrum, filtered singal, filtered spectrum and recovered siganl 
#variables need to be calculated in the main file
Vdm = 0
spectrum_demod = 0
spectrum_filtered = 0
filter = 0
Vr = 0
