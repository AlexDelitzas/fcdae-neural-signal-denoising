# -*- coding: utf-8 -*-
import tensorflow as tf 
import time
import numpy

from utils import loadData, resizeMultiChannelData, resizeData

class TFRecordDatasetBuilder:
    
    def __init__(self, dataset_folder, tfrecord_path, signal_file_names):
        self.dataset_folder = dataset_folder
        self.tfrecord_path = tfrecord_path
        self.signal_file_names = signal_file_names
        
    def write_record(self, X, y):
        tf_example = tf.train.Example(
                    features = tf.train.Features(feature={   
                        "X": tf.train.Feature(float_list=tf.train.FloatList(value=X.flatten())),
                        "y": tf.train.Feature(float_list=tf.train.FloatList(value=y.flatten())),
                    }))

        self.writer.write(tf_example.SerializeToString())
        
    def convert_to_windowed_data(self, data, targets):
        
        inputSize = int(512)
        stride = inputSize
        
        for i in range(0, data.shape[1]):
            data[:, i] = data[:, i] - data[:, i].mean()
            data[:, i] = data[:, i] / numpy.abs(data[:, i]).max()
             
        targets[:, 0] = targets[:, 0] - targets[:, 0].mean()
        ground_truth = targets[:, 0] 
        for i in range(1, targets.shape[1]):
            targets[:, i] = targets[:, i] - targets[:, i].mean()
            ground_truth += targets[:, i] 
        
        ground_truth /= numpy.abs(ground_truth).max()

        data = resizeMultiChannelData(data, inputSize, stride)
        targets = resizeData(ground_truth, inputSize, stride)
        
        return data, targets
                         
    def convert_to_record(self, signal_file_name):
        inputSignal = 'y'
        groundTruthSignal = 'ground_truth'
        fileFormat = 'mat'

        data, targets = loadData(self.dataset_folder, signal_file_name, fileFormat, inputSignal, groundTruthSignal)
    
        data, targets = self.convert_to_windowed_data(data, targets)
        print("\t Number of samples: " , targets.shape[0])
    
        tf_record_filename = self.tfrecord_path + "/" + signal_file_name + ".tfrecord"
        self.writer = tf.io.TFRecordWriter(tf_record_filename)
        for i in range(0, targets.shape[0]):
            try:
                self.write_record(data[i, :, :], targets[i])
            except IndexError:
                break
        self.writer.close()
        
    def create_dataset(self):
        for signal_file_name in self.signal_file_names:
            print("Handling signal file: " + signal_file_name)
            self.convert_to_record(signal_file_name)

start_time = time.time()

tfrecord_path = "../data/TFRecord/"
dataset_folder = "../data/mat/"

print("Generating dataset in path: " + tfrecord_path)
print("Reading data from data folder: " + dataset_folder)
print("============== Starting ==============")

noise_levels = [7, 9, 15, 20]
n_iterations = 10

signal_file_names = ['e_mix33_n' + str(noise_level) + '_iter' + str(iteration)\
                      for iteration in range(n_iterations) for noise_level in noise_levels]

tfrBuilder = TFRecordDatasetBuilder(dataset_folder = dataset_folder,
                                    tfrecord_path = tfrecord_path,
                                    signal_file_names = signal_file_names)
tfrBuilder.create_dataset()

print("Dataset generated at path: " + tfrecord_path)
print("Done in ", (time.time() - start_time) , " sec.")