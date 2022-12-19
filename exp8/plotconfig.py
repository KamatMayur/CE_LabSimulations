'''
authour: Mayur Kamat
affiliation: 201104032, TE-E&TC Engg. Sem V, 2021-22, GEC
last updated: 15/10/2022
'''

#importing necessary functions from libraries
from numpy import linspace, array
from scipy.fft import fftfreq


#message signal parameteres
amp = 10
fm = 3000

#these are sampling values
fs = 20*fm
dt= 1/fs
duration = 1
N = duration * fs

#generating time axis samples
time = linspace(0, duration, N)

#quantization parameters
n = 4
L = 2**n
step_size = (amp*2)/L
q_levels= array([i for i in range(L)] ) * step_size

#message and carrier singal variables need to be calculated in the main file
vm = 0

#spectrum variables needs to be calculated in the main file
spectrum = 0

#generating frequency axis samples
frequency = fftfreq(N, dt)


