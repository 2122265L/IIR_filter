#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 09:52:19 2017

@author: seiyu
"""

import IIRpy
import numpy as np
import pylab as pl

# Make a signal
fs = 1000
signal = np.fft.ifft(np.ones(fs))

y = np.zeros(fs)


def Filt(Ftype):
    N = 10
    fc = [290/fs, 310/fs, 390/fs, 420/fs, 460/fs]
    
    fws =[270/fs, 330/fs, 370/fs, 440/fs, 440/fs]
    
    f  = IIRpy.IIR(fc, Ftype, ord = N, ws = fws)
    
    for i in range(len(signal)):
        y[i] = f.filter(signal[i])
    
    pl.figure()
    pl.title("signal frequency for a %s, order %d" % (Ftype, N))
    pl.ylabel('f/Hz')
    pl.xlim(0,fs//2)
    pl.plot(np.arange(0,1000),abs(np.fft.fft(y)))
    
Ftype = ['lowpass', 'highpass', 'bandpass', 'bandstop']

for i in range(4):
    Filt(Ftype[i])
