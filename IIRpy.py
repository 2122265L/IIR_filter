#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 13:19:40 2017

@author: seiyu
"""

import numpy as np
from scipy.signal import butter, buttord

class __sos__:
    
    def __init__(self, a, b): 
        self.buffer1 = 0
        self.buffer2 = 0
        self.a1 = a[1]
        self.a2 = a[2]
        self.b0 = b[0]
        self.b1 = b[1]
        self.b2 = b[2]

    def filter(self, x):        
        acc_input = x - self.buffer1*self.a1 -self.buffer2*self.a2
        acc_output = acc_input*self.b0 + self.buffer1*self.b1 + self.buffer2*self.b2
        self.buffer2 = self.buffer1
        self.buffer1 = acc_input
        return acc_output

class IIR:
    
    """IIR Filter Class
    Combines butter and buttord functions to create a cascade of sencond order
    filters. The buttord function allows for more rigorous design, where
    the lowest order digital or analog Butterworth filter
    that loses no more than `gpass` dB in the passband and has at least
    `gstop` dB attenuation in the stopband can be specifid.
    
    Function
    --------
    IIRpy(wp, filter, **optional)
        optionals: ord, ws, gpass, gstop, nyq, analog
        
    Parameters
    ----------
    ord : int
        Defult = 6
        Order of the filter. This vaule
    filter: char
        lowpass  == low  == lp == l
        highpass == high == hp == h
        bandpass == pass == bp == p
        bandstop == stop == bs == s
    wp, ws : float
        Passband and stopband edge frequencies.
        For digital filters, these are normalized from 0 to 0.5, where 0.5 is the
        Nyquist frequency.  
        Example use:
            - Lowpass:   wp = 0.2,          ws = 0.3
            - Highpass:  wp = 0.3,          ws = 0.2
            - Bandpass:  wp = [0.2, 0.3],   ws = [0.1, 0.4]
            - Bandstop:  wp = [0.1, 0.6],   ws = [0.2, 0.5]
            
            - Multi Bandpass + Highpass:
                         wp = [0.10, 0.20, 0.30, 0.40, 0.45],
                         ws = [0.05, 0.25, 0.28, 0.43, 0.43]
            
            - Multi Bandstop + Lowpass:
                         wp = [0.10, 0.30, 0.40],   
                         ws = [0.15, 0.25, 0.45]
                         
        For analog filters, `wp` and `ws` are angular frequencies (e.g. rad/s).
    gpass : float 
        Defult = 3dB loss
        The maximum loss in the passband (dB). (+ve value)
    gstop : float
        Defult = 40dB loss
        The minimum attenuation in the stopband (dB). (+ve value)
    analog : bool, optional
        Defult = True
        When True, return an analog filter, otherwise a digital filter is
        returned.
    nyq : float
        Delfult = 0.5
        Option to normalise the nyquist frequency to any value.
        Defult is 0.5.
        
    Returns
    -------
    No values are returned after initialisation.
    
    Filtering
    ---------
    Real time filter:
        Single Input Single Output (SISO) filter, only accepts real values.
    
    
    Notes:  Analogue frequency == 'False' << has not been tested
            If any errors our found please forward on the error and inputs
            so that it can be fix
            
    """
    
    def __init2(self, _wp, ws, filter, *args):
        
        if ws is not None:
            order, _wp = buttord(_wp, ws, args[0], args[1])
            if (len(np.atleast_1d(_wp)) == 1) and (filter[0].lower() == 'b'):
                if filter == 'bandpass':
                    filter = 'highpass'
                else:
                    filter = 'lowpass'
        else:
            order = self.ord 

        
        #----------------------------------------------------------------------            
        _sos = butter(order, _wp, btype=filter, output='sos')
        
        a, b = np.zeros([len(_sos),3]), np.zeros([len(_sos),3])
        #----------------------------------------------------------------------        
        
        for i in range(len(_sos)):
            a[i] = _sos[i][3:]
            b[i] = _sos[i][:3]    
         
        self.sos.append(np.zeros(len(a)))        
        self.sos[self.flag] = [__sos__(a[i],b[i]) for i in range(len(a))]
        self.flag += 1
        
        return None
        #----------------------------------------------------------------------
        #---------------------------------------------------------------------- 
    
    def __filt_type(self, filter, _wp, ws):
        
        if (filter[0].lower() == 'l'):
            filter = 'lowpass'
            self.parrallel = False
            _wp = np.atleast_1d(_wp[0])
            if ws is not None: ws = np.atleast_1d(ws[0])

        elif (filter[0].lower() == 'h'):
            filter = 'highpass'
            self.parrallel = False
            _wp = np.atleast_1d(_wp[0])
            if ws is not None: ws = np.atleast_1d(ws[0])
            
        elif (filter.lower() == 'bp') | (filter.lower() == 'bandpass') | (filter[0].lower() == 'p'):
            filter = 'bandpass'
            self.parrallel = True
            
        elif (filter.lower() == 'bs') | (filter.lower() == 'bandstop') | (filter[0].lower() == 's'):
            filter = 'bandstop'
            self.parrallel = False

            
        return filter, _wp, ws
        #----------------------------------------------------------------------
        #----------------------------------------------------------------------
    
    def __init__(self, _wp, filter='lowpass', **optional):
        
        # optionals:
        ord = optional.get('ord', 6)
        ws = optional.get('ws', None)
        gpass = optional.get('gpass', 3)
        gstop = optional.get('gstop', 40)
        analog = optional.get('analog', True)
        nyq = optional.get('nyq', 0.5)
        
        self.ord = ord # order
        # number of cascaded 2nd order filter = repeat
        self.repeat = 1
        
        _wp = np.atleast_1d(_wp)
        _wp = [x/nyq for x in _wp]
        
        if ws is not None:
            ws = np.atleast_1d(ws)
            ws = [x/nyq for x in ws]
            if len(ws) != len(_wp): raise ValueError("lenght of ws and wp does not match")
            
        if not analog:
            _wp = [np.tan(np.pi * x / 2.0) for x in _wp]
            if ws is not None:
                ws  = [np.tan(np.pi * x / 2.0) for x in  ws]
                
        # standerdize the filter type
        filter, _wp, ws = IIR.__filt_type(self, filter, _wp, ws)
        cutoffs = len(_wp)
        
        #----------------------------------------------------------------------
        # Cascade filter coeficient seperation
        if (filter[0] == 'b') and cutoffs > 2:
            first_order_filter = 0
            
            if (cutoffs%2): 
                if (ws is None):
                    _wp = np.append(_wp,0.99999999)# extend filter to nyquist if need be
                    cutoffs += 1
                elif (ws is not None) & (len(ws)%2):
                    first_order_filter = 1
                
            self.repeat = cutoffs//2
            fc = []
            fc.append(np.zeros([self.repeat,2]))
            fc.append(np.zeros([first_order_filter])) 
            
            if ws is not None:
                
                fws = []
                fws.append(np.zeros([self.repeat,2]))
                fws.append(np.zeros([first_order_filter]))
                     
                if first_order_filter is not 0:
                    for i in range(self.repeat):
                        fc[0][i] = _wp[i*2:i*2+2]
                        fws[0][i] = ws[i*2:i*2+2]
                    fc[-1] =_wp[-1]
                    fws[-1]= ws[-1]
                else:
                    for i in range(self.repeat):
                        fc[i] = _wp[i*2:i*2+2]
                        fws[i] = ws[i*2:i*2+2]
                    
            else:    
                for i in range(self.repeat):
                    fc[0][i] = _wp[i*2:i*2+2]
            
            self.repeat += first_order_filter
                
        #----------------------------------------------------------------------        
        self.flag = 0
        self.sos= []
        
        if (cutoffs > 2) & (ws is None):
            for i in range(self.repeat):
                IIR.__init2(self, fc[0][i], None, filter)
                
        elif (cutoffs > 2) & (ws is not None):
            if (first_order_filter == 0):
                for i in range(self.repeat):
                    IIR.__init2(self, fc[i], fws[i], filter, gpass, gstop)
                    
            else:
                for i in range(len(fc[0])):
                    IIR.__init2(self, fc[0][i], fws[0][i], filter, gpass, gstop)
                    
                IIR.__init2(self, fc[1], fws[1], filter, gpass, gstop)
        
        else:
            IIR.__init2(self, _wp, ws, filter, gpass, gstop)
        #----------------------------------------------------------------------
        #----------------------------------------------------------------------
        self.iterator = [len(x) for x in self.sos]
        #----------------------------------------------------------------------

    def filter(self, x):
        
        if self.parrallel == False: 
            for j in range(self.repeat):
                for i in range(self.iterator[j]):
                    x = self.sos[j][i].filter(x)

            return np.real(x)
        else:
            X = 0
            for j in range(self.repeat):
                _x = 0
                for i in range(self.iterator[j]):
                    if i==0:_x = self.sos[j][i].filter(x)
                    else:_x = self.sos[j][i].filter(_x)     
                X += _x
            return np.real(X)
        #----------------------------------------------------------------------
        #----------------------------------------------------------------------
