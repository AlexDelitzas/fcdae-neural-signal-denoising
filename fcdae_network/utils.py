# -*- coding: utf-8 -*-
import numpy as np
import scipy.io as sio

def loadData(dataFolder, fileName, extension, inputSignalTag, groundTruthSignalTag, \
             groundTruthSpikeTimeTrainTag):
  mat = sio.loadmat(dataFolder + '/' + fileName + '.' + extension)

  y = mat[inputSignalTag]
  groundTruth = mat[groundTruthSignalTag]
  
  groundTruthSpikeTimes = None
  if groundTruthSpikeTimeTrainTag != None:
      mat = sio.loadmat(dataFolder + '/' + fileName + '_spikes' + '.' + extension)
      groundTruthSpikeTimes = mat[groundTruthSpikeTimeTrainTag]

  return y, groundTruth, groundTruthSpikeTimes

def loadSpikeTrainData(dataFolder, fileName, extension, inputSignalTag, groundTruthSignalTag):
  mat = sio.loadmat(dataFolder + '/' + fileName + '_spikes.' + extension)

  return mat['groundTruthSpikeTimeTrain']

def loadTestData(dataFolder, fileName, extension, inputSignalTag, groundTruthSignalTag):
  mat = sio.loadmat(dataFolder + '/' + fileName + '.' + extension)

  y = mat['out_data']

  return y

def resizeData(data, inputSize, stride):
  output = []
  for i in range(0, len(data), stride):
    if i + inputSize > len(data):
      break
    output.append(data[i:i+inputSize])
  output_array = np.transpose(np.stack(output, axis = 1))
  
  return output_array


def resizeMultiChannelData(data, inputSize, stride):
  output = []
  for i in range(0, len(data), stride):
    if i + inputSize > len(data):
      break
    output.append(data[i:i+inputSize, :])
  output_array = np.stack(output, axis = 1)
  
  output_array = np.swapaxes(output_array, 0, 1)
  
  return output_array

def resizeToTimeseries(data):
  return data.ravel()

def resizeToTimeseriesMultiChannel(data):
    output_array  = np.zeros((data.shape[0] * data.shape[1], data.shape[2]))
    for i in range(0, data.shape[2]):
        output_array[:, i] = data[:, :, i].ravel()
        
    return output_array
    
    
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