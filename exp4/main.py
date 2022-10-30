'''
authour: Mayur Kamat
affiliation: 201104032, TE-E&TC Engg. Sem V, 2021-22, GEC
last updated: 15/10/2022
'''

#importing necessary functions from libraries
from array import array
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
from numpy import cos, sin, fft, abs
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
    Vm = amp * cos(2*pi*freq*time)

    #calculating the AM signals
    Vfm = carrierAmp * cos(2*pi*carrierFreq*time + ((kf * amp) / freq) * sin(2*pi*freq*time))   #FM

    #calculating mf
    mf = (amp * kf) / freq
 
    #calculating the FFT of FM signal
    spectrum = abs(fft.fft(Vfm))
    spectrum_plt = spectrum[idx]/N #sorting the indices and scaling the magnitude for plotting purpose 

    #calculating the bandwidth by counting number of sidebands with significant value
    BW = 0
    for f in range(carrierFreq, int(spectrum.size/2)):
        if spectrum[f]/N > BWThreshold:
            BW = f
    BW = (BW - carrierFreq) * 2

    #functions below plot the singals
    def plot_carrier():
        ax.clear()
        ax.set_xlabel('time - (sec)')
        ax.set_ylabel('amplitude - (volts)')
        ax.set_title('carrier')
        ax.plot(time[:2000], Vc[:2000], 'b', label='Carrier') 

    def plot_m():
        ax.clear()
        ax.set_xlabel('time - (sec)')
        ax.set_ylabel('amplitude - (volts)')
        ax.set_title('Modulating signal')
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
        ax.text(0.05, 0.95, "Mf = " + str(round(mf, 4)) + '\n' + 'BW = ' + str(BW), transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=bbox)
        ax.plot(frequency_plt[90000:110000], spectrum_plt[90000:110000], 'b', label='FM spectrum')


    #dictionary to call the plotting functins as and when the graph slider value changes
    GraphSelector = {
        0 : plot_carrier,
        1 : plot_m,
        2 : plot_fm,
        3 : plot_spectrum  
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
def update_Freq(val):
    global freq
    freq = val
    plotSingals()

def update_amp(val):
    global amp
    amp = val
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
ax_kf = plt.axes([0.17, 0.11, 0.65, 0.03])
kf_Slider = Slider(ax_kf, 'Kf', valmin=0, valmax=500, valstep=10, valinit=kf)

ax_freq = plt.axes([0.17, 0.15, 0.65, 0.03])
freqSlider = Slider(ax_freq, 'freq', valmin=100, valmax=800, valstep=10, valinit=freq)

ax_amp = plt.axes([0.17, 0.19, 0.65, 0.03])
ampSlider = Slider(ax_amp, 'amp', valmin=0, valmax=15, valstep=0.1, valinit=amp)

ax_graph = plt.axes([0.17, 0.23, 0.65, 0.03])
graph_Slider = Slider(ax_graph, 'Graph Select', valmin=0, valmax=3, valstep=1, valinit=0)

#plots the signal on run
plotSingals()

#handles updates on the sliders widgets
ampSlider.on_changed(update_amp)
freqSlider.on_changed(update_Freq)
graph_Slider.on_changed(update_graph)
kf_Slider.on_changed(update_kf)

#needed in vscode to plot the fig in a new window...can be ignored in spyder
plt.show()
