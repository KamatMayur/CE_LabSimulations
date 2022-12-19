'''
authour: Mayur Kamat
affiliation: 201104032, TE-E&TC Engg. Sem V, 2021-22, GEC
last updated: 22/11/2022
'''

#importing necessary functions from libraries
from numpy import linspace
from numpy.fft import fftfreq


#message signal parameteres
amp_vm = 20
amp_vc = 50
fc = 800

#these are sampling values
fs = 30*fc
dt= 1/fs
duration = 1
N = duration * fs

#generating time axis samples
time = linspace(0, duration, N)

#message and carrier singal variables need to be calculated in the main file
vm = 0
vc = 0
vask = 0

#spectrum variables needs to be calculated in the main file
spectrum = 0

#generating frequency axis samples
frequency = fftfreq(len(time), dt)
print(len(frequency))


