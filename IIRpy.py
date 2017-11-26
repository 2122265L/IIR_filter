#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 09:52:19 2017

@author: seiyu
"""

if __name__ == "__main__":

    import numpy as np
    from scipy.signal import butter
    
    class IIR:
        """
        IIR filter Class
        
        Takes initialiseation inputs:
            Order: of filter, defult = 2
            Cut off frequencies: normalised to nyquist = 0.5
            filter type: low, high, pass, stop
            
        Real time filter:
            Single Input Single Output (SISO) filter 
        
        Coeficients can be extracted:
            numerator coeficients = self.b
            denomiator coeficients = self.a
        """
        
        def init2(self, _N, _fc, filter):
            
            #---------------------------------------------------------------------            
            _sos = butter(self.N, _fc, btype=filter, output='sos')
            
            a, b = np.zeros([_N,3]), np.zeros([_N,3])
            # sos stores the 'b's then the 'a's 
            for i in range(_N):
                a[i] = _sos[i][3:]
                b[i] = _sos[i][:3]    
            
            return a, b
            #----------------------------------------------------------------------
            #----------------------------------------------------------------------
            
        def init_coefs(self):
            
            self.a, self.b = np.zeros([self.repeat,self.factor,3]), np.zeros([self.repeat,self.factor,3])
            self.buffer1, self.buffer2  = np.zeros([self.repeat, self.factor]), np.zeros([self.repeat, self.factor])
            
            return None
            #----------------------------------------------------------------------
            #----------------------------------------------------------------------   
        
        def filt_type(self, filter, _fc):
            
            if (filter[0].lower() == 'l'):
                filter = 'lowpass'
                self.parrallel = False
                self.factor = self.N//2 + self.N%2
                _fc = np.atleast_1d(_fc[0])
                
            elif (filter[0].lower() == 'h'):
                filter = 'highpass'
                self.parrallel = False
                self.factor = self.N//2 + self.N%2
                _fc = np.atleast_1d(_fc[0])
                
            elif (filter.lower() == 'bp') | (filter.lower() == 'bandpass') | (filter[0].lower() == 'p'):
                filter = 'bandpass'
                self.parrallel = True
                
            elif (filter.lower() == 'bs') | (filter.lower() == 'bandstop') | (filter[0].lower() == 's'):
                filter = 'bandstop'
                self.parrallel = False
    
                
            return filter, _fc
            #----------------------------------------------------------------------
            #----------------------------------------------------------------------
        
        def __init__(self, _N=2, _fc, filter='lowpass'):
            
            # turn _fc into an array
            _fc = np.atleast_1d(_fc) 
            # set nyq frequency as 1 for butter function
            _fc = [2*x for x in _fc] 
            # make sure cutoff frequencies are properly ordered
            _fc = sorted(_fc)
            cutoffs = len(_fc)
            
            self.N = _N # order
            self.factor = _N
            # number of loops cascaded 2nd order filter = repeat
            self.repeat = 1
            
            # standerdize the filter type
            filter, _fc = IIR.filt_type(self, filter, _fc)
            
            #----------------------------------------------------------------------
            # Cascade filter actualisation 
            if ((filter == 'bandpass') or (filter == 'bandstop')) and cutoffs > 2:
                fc = _fc
                
                if cutoffs%2: 
                    _fc = np.append(_fc,1)# extend filter to nyquist if need be
                    cutoffs += 1
                
                self.repeat = cutoffs//2
                fc = np.zeros([self.repeat,2])
                for i in range(self.repeat):
                    fc[i] = _fc[i*2:i*2+2]
            #----------------------------------------------------------------------
            IIR.init_coefs(self)
            
            if cutoffs > 2:
                for i in range(self.repeat):
                    self.a[i], self.b[i] = IIR.init2(self, _N, fc[i], filter)
            else:
                self.a[0], self.b[0] = IIR.init2(self, self.factor, _fc, filter)
            #----------------------------------------------------------------------
            #----------------------------------------------------------------------
                
        def workhorse(self, x, j):
            
            for i in range(self.factor):
                acc_input = x - self.buffer1[j][i]*self.a[j][i][1] -self.buffer2[j][i]*self.a[j][i][2]
                x = (acc_input*self.b[j][i][0] + self.buffer1[j][i]*self.b[j][i][1] + self.buffer2[j][i]*self.b[j][i][2])*self.a[j][i][0]
                self.buffer2[j][i] = self.buffer1[j][i]
                self.buffer1[j][i] = acc_input
    
            return x
            #----------------------------------------------------------------------
            #----------------------------------------------------------------------
            
        def filter(self, x):
            
            if self.parrallel == False: 
                for j in range(self.repeat):
                    x = IIR.workhorse(self, x, j)
                return x
            else:
                _x = 0
                for j in range(self.repeat):
                    _x += IIR.workhorse(self, x, j)
                return _x
            #----------------------------------------------------------------------
            #----------------------------------------------------------------------