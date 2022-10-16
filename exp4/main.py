'''
authour: Mayur Kamat
affiliation: 201104032, TE-E&TC Engg. Sem V, 2021-22, GEC
last updated: 15/10/2022
'''

#importing necessary functions from libraries
from array import array
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
from numpy import cos, fft, abs
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

    #calulating carrier
    Vc = carrierAmp * cos(2*pi*carrierFreq*time)

    #calculating the message signals
    Vm1 = amp1 * cos(2*pi*m1freq*time)
    Vm2 = amp2 * cos(2*pi*m2freq*time)
    Vm = Vm1 + Vm2
   
    #calculating the AM signals
    Vfm = carrierAmp * cos(2*pi*carrierFreq*time + (kf/max(m1freq, m2freq)) * Vm)   #FM

    #calculating mf
    mf = max(Vm)*kf/max(m1freq, m2freq)

    #calculating the bandwidth using Carson's Rule
    BW = 2 * max(m1freq, m2freq) * (1 + mf)
 
    #calculating the FFT of FM signal
    spectrum = abs(fft.fft(Vfm))
    spectrum_plt = spectrum[idx]/N #sorting the indices and scaling the magnitude for plotting purpose 


    #functions below plot the singals
    def plot_carrier():
        ax.clear()
        ax.set_xlabel('time - (sec)')
        ax.set_ylabel('amplitude - (volts)')
        ax.set_title('carrier')
        ax.plot(time[:2000], Vc[:2000], 'b', label='Carrier')

    def plot_m1():
        ax.clear()
        ax.set_xlabel('time - (sec)')
        ax.set_ylabel('amplitude - (volts)')
        ax.set_title('Tone 1')
        ax.plot(time[:2000], Vm1[:2000], 'b', label='Tone 1')

    def plot_m2():
        ax.clear()
        ax.set_xlabel('time - (sec)')
        ax.set_ylabel('amplitude - (volts)')
        ax.set_title('Tone 2')
        ax.plot(time[:2000], Vm2[:2000], 'b', label='Tone 2')

    def plot_m():
        ax.clear()
        ax.set_xlabel('time - (sec)')
        ax.set_ylabel('amplitude - (volts)')
        ax.set_title('2 Tone Modulating signal')
        ax.plot(time[:2000], Vm[:2000], 'b', label='Message')

    def plot_fm():
        ax.clear()
        ax.set_xlabel('time - (sec)')
        ax.set_ylabel('amplitude - (volts)')
        ax.set_title('Modulated signal')
        ax.plot(time[:2000], Vfm[:2000], 'b', label='FM signal')

    def plot_spectrum(): 
        ax.clear()
        ax.set_xlabel('frequency - (hertz)')
        ax.set_ylabel('Amplitude - (volts)')
        ax.set_title('Spectrum')
        bbox= dict(boxstyle='round', alpha=0.5)
        ax.text(0.05, 0.95, "Mf = " + str(round(mf, 4)) + '\n' + 'BW', transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=bbox)
        ax.plot(frequency_plt[90000:110000], spectrum_plt[90000:110000], 'b', label='FM spectrum')


    #dictionary to call the plotting functins as and when the graph slider value changes
    GraphSelector = {
        0 : plot_carrier,
        1 : plot_m1,
        2 : plot_m2,
        3 : plot_m,
        4 : plot_fm,
        5 : plot_spectrum  
        }

    GraphSelector.get(CurrentGraph)()
        
    #plot adjustments
    fig1.tight_layout(h_pad=2)
    fig1.set_size_inches(12, 7)
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

def update_kf(val):
    global kf
    kf = val
    plotSingals()


#slider widgets
ax_kf = plt.axes([0.17, 0.07, 0.65, 0.03])
kf_Slider = Slider(ax_kf, 'Kf', valmin=0, valmax=500, valstep=10, valinit=kf)

ax_m1freq = plt.axes([0.17, 0.11, 0.65, 0.03])
m1_freqSlider = Slider(ax_m1freq, 'm1 freq', valmin=100, valmax=800, valstep=10, valinit=m1freq)

ax_m2freq = plt.axes([0.17, 0.15, 0.65, 0.03])
m2_freqSlider = Slider(ax_m2freq, 'm2 freq', valmin=100, valmax=800, valstep=10, valinit=m2freq)

ax_amp1 = plt.axes([0.17, 0.19, 0.65, 0.03])
m1_Slider = Slider(ax_amp1, 'amp1', valmin=0, valmax=15, valstep=0.1, valinit=amp1)

ax_amp2 = plt.axes([0.17, 0.23, 0.65, 0.03])
m2_Slider = Slider(ax_amp2, 'amp2', valmin=0, valmax=15, valstep=0.1, valinit=amp2)

ax_graph = plt.axes([0.17, 0.27, 0.65, 0.03])
graph_Slider = Slider(ax_graph, 'Graph Select', valmin=0, valmax=5, valstep=1, valinit=0)

#plots the signal on run
plotSingals()

#handles updates on the sliders widgets
m1_Slider.on_changed(update_amp1)
m2_Slider.on_changed(update_amp2)
m1_freqSlider.on_changed(update_m1Freq)
m2_freqSlider.on_changed(update_m2Freq)
graph_Slider.on_changed(update_graph)
kf_Slider.on_changed(update_kf)

#needed in vscode to plot the fig in a new window...can be ignored in spyder
plt.show()
