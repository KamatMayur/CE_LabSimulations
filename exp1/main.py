'''
authour: Mayur Kamat
affiliation: 201104032, TE-E&TC Engg. Sem V, 2021-22, GEC
last updated: 15/10/2022
'''

#importing necessary functions from libraries
from array import array
from matplotlib import pyplot as plt 
from matplotlib.widgets import Slider
from numpy import cos, arange, linspace, fft, abs, argsort, array
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
    Vm1 = carrierAmp * ma1 * cos(2*pi*m1freq*time)
    Vm2 = carrierAmp * ma2 * cos(2*pi*m2freq*time)
    Vm = Vm1 + Vm2
   
    #calculating the AM signals
    Vam = carrierAmp * ( 1 + Vm/carrierAmp) * cos(2*pi*carrierFreq*time)  #AM
    Vdsbsc = (Vm1 + Vm2) * cos(2*pi*carrierFreq*time) #DSB-SC
    
    #demodulating the AM singal
    Vdm = Vdsbsc * cos(2*pi*carrierFreq*time) #demodulation is performed on the DSB-SC

    #calculating the FFT of AM signal
    spectrum = abs(fft.fft(Vam))
    spectrum_plt = spectrum[idx]/N #sorting the indices and scaling the magnitude for plotting purpose 

    #calculating the FFT of demodulated signal 
    spectrum_demod = abs(fft.fft(Vdm))
    spectrum_demod_plt = spectrum_demod[idx]/N #sorting the indices and scaling the magnitude for plotting purpose

    #designing the ideal lowpass filter
    filter = array([0]*(frequency.size))
    for f in range(frequency.size):
        if frequency[f] > -BW/2 and frequency[f] < BW/2:
            filter[f] = 1

    filter_plt = filter[idx] #sorting the indices and scaling the magnitude for plotting purpose

    #multiplying the filters spectrum with the demodulated signal to recovers the message
    spectrum_filtered = spectrum_demod * filter

    #taking the inverse of the filtered spectrum to get the singal back
    Vr = fft.ifft(spectrum_filtered)

    #functions below plot the singals
    def plot_carrier():
        ax.clear()
        ax.set_xlabel('time - (sec)')
        ax.set_ylabel('amplitude - (volts)')
        ax.set_title('carrier')
        Vm1 = carrierAmp * ma1 * cos(2*pi*m1freq*time)
        ax.plot(time[:2000], Vc[:2000], 'b', label='Carrier')

    def plot_m1():
        ax.clear()
        ax.set_xlabel('time - (sec)')
        ax.set_ylabel('amplitude - (volts)')
        ax.set_title('Tone 1')
        Vm1 = carrierAmp * ma1 * cos(2*pi*m1freq*time)
        ax.plot(time[:2000], Vm1[:2000], 'b', label='Tone 1')

    def plot_m2():
        ax.clear()
        ax.set_xlabel('time - (sec)')
        ax.set_ylabel('amplitude - (volts)')
        ax.set_title('Tone 2')
        Vm2 = carrierAmp * ma2 * cos(2*pi*m2freq*time)
        ax.plot(time[:2000], Vm2[:2000], 'b', label='Tone 2')

    def plot_m():
        ax.clear()
        ax.set_xlabel('time - (sec)')
        ax.set_ylabel('amplitude - (volts)')
        ax.set_title('2 Tone Modulating signal')
        Vm2 = carrierAmp * ma2 * cos(2*pi*m2freq*time)
        ax.plot(time[:2000], Vm[:2000], 'b', label='Message')

    def plot_am():
        ax.clear()
        ax.set_xlabel('time - (sec)')
        ax.set_ylabel('amplitude - (volts)')
        ax.set_title('Modulated signal')
        Vam = carrierAmp * ( 1 + ma1 * cos(2*pi*m1freq*time) + ma2 * cos(2*pi*m2freq*time)) * cos(2*pi*carrierFreq*time)
        ax.plot(time[:2000], Vam[:2000], 'b', label='AM signal')

    def plot_spectrum(): 
        ax.clear()
        ax.set_xlabel('frequency - (hertz)')
        ax.set_ylabel('Amplitude - (volts)')
        ax.set_title('Spectrum')
        ax.plot(frequency_plt[90000:110000], spectrum_plt[90000:110000], 'b', label='AM spectrum')

    def plot_demodSpectrum():
        ax.clear()
        ax.set_xlabel('frequency - (hertz)')
        ax.set_ylabel('Amplitude - (volts)')
        ax.set_title('Demodulated spectrum')
        ax.plot(frequency_plt[95000:105000], spectrum_demod_plt[95000:105000], 'b', label='demodulated spectrum')
        ax.plot(frequency_plt[95000:105000], filter_plt[95000:105000], 'g', label='filter spectrum')
              
    def plot_recoveredSignal():
        ax.clear()
        ax.set_xlabel('time - (sec)')
        ax.set_ylabel('amplitude - (volts)')
        ax.set_title('recovered signal')
        ax.plot(time[:2000], Vr[:2000], 'b', label='Recovered signal')

    #dictionary to call the plotting functins as and when the graph slider value changes
    GraphSelector = {
        0 : plot_carrier,
        1 : plot_m1,
        2 : plot_m2,
        3 : plot_m,
        4 : plot_am,
        5 : plot_spectrum,
        6 : plot_demodSpectrum,
        7 : plot_recoveredSignal
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

def update_ma1(val):
    global ma1
    ma1 = val
    plotSingals()

def update_ma2(val):
    global ma2
    ma2 = val
    plotSingals()

def update_graph(val):
    global CurrentGraph
    CurrentGraph = val
    plotSingals()

def update_bw(val):
    global BW
    BW = val
    plotSingals()


#slider widgets
ax_bw = plt.axes([0.17, 0.07, 0.65, 0.03])
bw_Slider = Slider(ax_bw, 'BW', valmin=50, valmax=1500, valstep=100, valinit=BW)

ax_m1freq = plt.axes([0.17, 0.11, 0.65, 0.03])
m1_freqSlider = Slider(ax_m1freq, 'm1 freq', valmin=100, valmax=800, valstep=10, valinit=m1freq)

ax_m2freq = plt.axes([0.17, 0.15, 0.65, 0.03])
m2_freqSlider = Slider(ax_m2freq, 'm2 freq', valmin=100, valmax=800, valstep=10, valinit=m2freq)

ax_m1 = plt.axes([0.17, 0.19, 0.65, 0.03])
m1_Slider = Slider(ax_m1, 'ma1', valmin=0, valmax=0.9, valstep=0.02, valinit=ma1)

ax_m2 = plt.axes([0.17, 0.23, 0.65, 0.03])
m2_Slider = Slider(ax_m2, 'ma2', valmin=0, valmax=0.9, valstep=0.02, valinit=ma2)

ax_graph = plt.axes([0.17, 0.27, 0.65, 0.03])
graph_Slider = Slider(ax_graph, 'Graph Select', valmin=0, valmax=7, valstep=1, valinit=0)

#plots the signal on run
plotSingals()

#handles updates on the sliders widgets
m1_Slider.on_changed(update_ma1)
m2_Slider.on_changed(update_ma2)
m1_freqSlider.on_changed(update_m1Freq)
m2_freqSlider.on_changed(update_m2Freq)
graph_Slider.on_changed(update_graph)
bw_Slider.on_changed(update_bw)

#needed in vscode to plot the fig in a new window...can be ignored in spyder
plt.show()
