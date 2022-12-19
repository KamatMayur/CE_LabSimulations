'''
authour: Mayur Kamat
affiliation: 201104032, TE-E&TC Engg. Sem V, 2021-22, GEC
last updated: 22/11/2022
'''

#importing necessary functions from libraries
from matplotlib import pyplot as plt 
from matplotlib.widgets import Slider
from numpy import cos, real, abs
from numpy.fft import fft
from math import pi
from scipy.fft import fft
from plotconfig import *

#global (fig, ax) tuple, making it global makes it easier to update values and use GUI
fig1, ax = plt.subplots()

#keeps track of the currently displayed plot
CurrentGraph = 0

#plots, calculates and updates the signals using the global variables from plotconfig
#which are updated in the update functions below
def plotSingals():
    global fig1, ax

    #producing the message and carrier signals
    vm = 0*time
    vm[:120] = amp_vm
    vc = amp_vc*cos(2*pi*fc*time)

    #ASK signal
    vask = vm*vc
    
    #calculating the FFT
    spectrum = (fft(vask))

    #functions below plot the singals
    def plot_vm():
        ax.clear()
        ax.set_xlabel('time - (sec)')
        ax.set_ylabel('amplitude - (volts)')
        ax.set_title('message and quantized signal')
        ax.plot(time[:400], vm[:400], 'b', label='Message')

    def plot_vc():
        ax.clear()
        ax.set_xlabel('time - (sec)')
        ax.set_ylabel('amplitude - (volts)')
        ax.set_title('Carrier Signal')
        ax.plot(time[:400], vc[:400], 'b', label='Carrier')
    
    def plot_vask():
        ax.clear()
        ax.set_xlabel('time - (sec)')
        ax.set_ylabel('amplitude - (volts)')
        ax.set_title('ASK signal')
        ax.plot(time[:400], vask[:400], 'r', label='Vask')

    def plot_spectrum(): 
        ax.clear()
        ax.set_xlabel('frequency - (hertz)')
        ax.set_ylabel('Amplitude - (volts)')
        ax.set_title('ASK spectrum')
        ax.plot(frequency, abs((real((spectrum)))/N), 'b', label='spectrum')
        ax.set_xlim(-1500, 1500)


    #dictionary to call the plotting functins as and when the graph slider value changes
    GraphSelector = {
        0 : plot_vm,
        1 : plot_vc,
        2 : plot_vask,
        3 : plot_spectrum,
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


def update_graph(val):
    global CurrentGraph
    CurrentGraph = val
    plotSingals()




#slider widgets
ax_graph = plt.axes([0.17, 0.27, 0.65, 0.03])
graph_Slider = Slider(ax_graph, 'Graph Select', valmin=0, valmax=3, valstep=1, valinit=0)

#plots the signal on run
plotSingals()

#handles updates on the sliders widgets
graph_Slider.on_changed(update_graph)

#needed in vscode to plot the fig in a new window...can be ignored in spyder
plt.show()
