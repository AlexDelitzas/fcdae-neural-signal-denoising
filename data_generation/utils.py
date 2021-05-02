# -*- coding: utf-8 -*-
import numpy as np
import scipy.io as sio
from scipy.signal import find_peaks


def loadData(dataFolder, fileName, extension, inputSignalTag, groundTruthSignalTag):
  mat = sio.loadmat(dataFolder + '/' + fileName + '.' + extension)

  y = mat[inputSignalTag]
  groundTruth = mat[groundTruthSignalTag]
  
  return y, groundTruth


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