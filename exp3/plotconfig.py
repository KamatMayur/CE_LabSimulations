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

#message signal parameteres
amp1 = 3
amp2 = 6
m1freq = 200
m2freq = 600

#filter parameters 
BW = 50
centerFreq = 100

#message and carrier singal variables need to be calculated in the main file
Vm1 = 0
Vm2 = 0
Vm = 0

#spectrum variables needs to be calculated in the main file
spectrum = 0
m1spectrum = 0
m2spectrum = 0

#generating frequency axis samples
frequency = fft.fftfreq(N, dt)

#sorting frequency axis indices for plotting purpose
idx = argsort(frequency)
frequency_plt = frequency[idx]

#filtered spectrum and recovered siganl 
#variables need to be calculated in the main file
filter = 0
Vr = 0
