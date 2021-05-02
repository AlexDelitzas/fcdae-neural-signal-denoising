# -*- coding: utf-8 -*-
import numpy as np
import scipy.io as sio
    
def calculateSNRImprovement(testX, testy, predictions):
    SNR_imp = 10 * np.log10(np.sum(np.square(testX - testy), axis = 0) \
                        / np.sum(np.square(predictions - testy), axis = 0))
    
    SNR_before =  10 * np.log10(np.mean(np.square(testy), axis = 0) \
                                / np.mean(np.square(testX - testy), axis = 0))
        
    SNR_after =  10 * np.log10(np.mean(np.square(testy), axis = 0) \
                                / np.mean(np.square(predictions - testy), axis = 0))  
        
    return SNR_before, SNR_after, SNR_imp

def calculateRMSE(testy, predictions):
    return np.sqrt(np.mean(np.square(testy - predictions), axis = 0))