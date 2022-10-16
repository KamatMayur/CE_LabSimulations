'''
authour: Mayur Kamat
affiliation: 201104032, TE-E&TC Engg. Sem V, 2021-22, GEC
last updated: 15/10/2022
'''

#importing necessary functions from libraries
from array import array
from matplotlib import pyplot as plt 
from matplotlib.widgets import Slider
from numpy import cos, fft, abs, array
from math import pi
from plotconfig import *

#global (fig, ax) tuple, making it global makes it easier to update values and use GUI
fig1, ax = plt.subplots()

#keeps track of the currently displayed plot
CurrentGraph = 0

#plots, calculates and updates the signals using the global variables from plotconfig
#which are updated in the update functions below
def plotSingals():
    global fig1, ax
    
    #calculating the message signals
    Vm1 = amp1 * cos(2*pi*m1freq*time)
    Vm2 = amp2 * cos(2*pi*m2freq*time)
    Vm = Vm1 + Vm2
    
    #calculating the FFT of multiplexed signal
    spectrum = abs(fft.fft(Vm))
    spectrum_plt = spectrum[idx]/N #sorting the indices and scaling the magnitude for plotting purpose 

    #designing the ideal bandpass filter
    filter = array([0]*(frequency.size))
    for f in range(frequency.size):
        if frequency[f] > -centerFreq-BW/2 and frequency[f] < -centerFreq+BW/2 or frequency[f] > centerFreq-BW/2 and frequency[f] < centerFreq+BW/2:
            filter[f] = 1

    filter_plt = filter[idx] #sorting the indices and scaling the magnitude for plotting purpose

    #multiplying the filters spectrum with the FDM spectrum to recover the message
    spectrum_filtered = spectrum * filter

    #taking the inverse of the filtered spectrum to get the signal back
    Vr = fft.ifft(spectrum_filtered)

    #functions below plot the singals
    def plot_m1():
        ax.clear()
        ax.set_xlabel('time - (sec)')
        ax.set_ylabel('amplitude - (volts)')
        ax.set_title('message 1')
        ax.plot(time[:2000], Vm1[:2000], 'b', label='Message 1')

    def plot_m2():
        ax.clear()
        ax.set_xlabel('time - (sec)')
        ax.set_ylabel('amplitude - (volts)')
        ax.set_title('message 2')
        ax.plot(time[:2000], Vm2[:2000], 'b', label='Meassage 2')
    
    def plot_m():
        ax.clear()
        ax.set_xlabel('time - (sec)')
        ax.set_ylabel('amplitude - (volts)')
        ax.set_title('multiplexed signal')
        ax.plot(time[:2000], Vm[:2000], 'b', label='Multiplexed Signal')

    def plot_spectrum(): 
        ax.clear()
        ax.set_xlabel('frequency - (hertz)')
        ax.set_ylabel('Amplitude - (volts)')
        ax.set_title('FDM Spectrum')
        ax.plot(frequency_plt[97500:102500], spectrum_plt[97500:102500], 'b', label='FDM Spectrum')

    def plot_demultiplexedSpectrum():
        ax.clear()
        ax.set_xlabel('frequency - (hertz)')
        ax.set_ylabel('Amplitude - (volts)')
        ax.set_title('Demultiplexed spectrum')
        ax.plot(frequency_plt[97500:102500], spectrum_plt[97500:102500], 'b', label='demultiplexed spectrum')
        ax.plot(frequency_plt[97500:102500], filter_plt[97500:102500], 'g', label='filter spectrum')
              
    def plot_recoveredSignal():
        ax.clear()
        ax.set_xlabel('time - (sec)')
        ax.set_ylabel('amplitude - (volts)')
        ax.set_title('recovered signal')
        ax.plot(time[:2000], Vr[:2000], 'b', label='Recovered signal')


    #dictionary to call the plotting functins as and when the graph slider value changes
    GraphSelector = {
        0 : plot_m1,
        1 : plot_m2,
        2 : plot_m,
        3 : plot_spectrum,
        4 : plot_demultiplexedSpectrum,
        5 : plot_recoveredSignal,
        }

    GraphSelector.get(CurrentGraph)()
        
    #plot adjustments
    fig1.tight_layout(h_pad=2)
    fig1.set_size_inches(14, 7)
    plt.subplots_adjust(bottom=0.4)

    #draws the plot
    ax.grid(True)
    ax.legend()
    plt.draw()


#functions below update global parameters 
def update_m1Freq(val):
    global m1freq
    m1freq = val
    plotSingals()

def update_m2Freq(val):
    global m2freq
    m2freq = val
    plotSingals()

def update_amp1(val):
    global amp1
    amp1 = val
    plotSingals()

def update_amp2(val):
    global amp2
    amp2 = val
    plotSingals()

def update_graph(val):
    global CurrentGraph
    CurrentGraph = val
    plotSingals()

def update_bw(val):
    global BW
    BW = val
    plotSingals()

def update_centerFreq(val):
    global centerFreq
    centerFreq = val
    plotSingals()


#slider widgets
ax_bw = plt.axes([0.17, 0.03, 0.65, 0.03])
bw_Slider = Slider(ax_bw, 'BW', valmin=100, valmax=400, valstep=25, valinit=BW)

ax_centerFreq = plt.axes([0.17, 0.07, 0.65, 0.03])
centerFreq_Slider = Slider(ax_centerFreq, 'Center Freq', valmin=0, valmax=1000, valstep=10, valinit=centerFreq)

ax_m1freq = plt.axes([0.17, 0.11, 0.65, 0.03])
m1_freqSlider = Slider(ax_m1freq, 'm1 freq', valmin=100, valmax=800, valstep=10, valinit=m1freq)

ax_m2freq = plt.axes([0.17, 0.15, 0.65, 0.03])
m2_freqSlider = Slider(ax_m2freq, 'm2 freq', valmin=100, valmax=800, valstep=10, valinit=m2freq)

ax_amp1 = plt.axes([0.17, 0.19, 0.65, 0.03])
m1_Slider = Slider(ax_amp1, 'amp1', valmin=1, valmax=10, valstep=0.1, valinit=amp1)

ax_amp2 = plt.axes([0.17, 0.23, 0.65, 0.03])
m2_Slider = Slider(ax_amp2, 'amp2', valmin=1, valmax=10, valstep=0.1, valinit=amp2)

ax_graph = plt.axes([0.17, 0.27, 0.65, 0.03])
graph_Slider = Slider(ax_graph, 'Graph Select', valmin=0, valmax=5, valstep=1, valinit=0)

#plots the signal on run
plotSingals()

#handles updates on the sliders widgets
m1_Slider.on_changed(update_amp1)
m2_Slider.on_changed(update_amp2)
m1_freqSlider.on_changed(update_m1Freq)
m2_freqSlider.on_changed(update_m2Freq)
bw_Slider.on_changed(update_bw)
centerFreq_Slider.on_changed(update_centerFreq)
graph_Slider.on_changed(update_graph)

#needed in vscode to plot the fig in a new window...can be ignored in spyder
plt.show()
