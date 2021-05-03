# -*- coding: utf-8 -*-
import scipy.io as sio
import numpy as np

import tensorflow as tf
from random import shuffle

import random

from models import create_fcdae
from utils import calculateSNRImprovement, calculateRMSE
    

# Change device to "CPU" if you want to run tensorflow on your CPU.
use_device = "GPU"

if (use_device == "GPU"):
    physical_devices = tf.config.experimental.list_physical_devices('GPU')
    assert len(physical_devices) > 0, "Not enough GPU hardware devices available"
    config = tf.config.experimental.set_memory_growth(physical_devices[0], True)

batch_size = 8
noise_level = 7

def _parse_function(example_proto):
    keys_to_features = {

        'X': tf.io.FixedLenFeature((512, 4), tf.float32),
        'y':tf.io.FixedLenFeature((512), tf.float32)
        }
    
    parsed_features = tf.io.parse_single_example(example_proto, keys_to_features)
    X = parsed_features['X']
    y = parsed_features['y']
    return X, tf.transpose([y, y, y, y])

##############################################################################
SNRs = []
RMSEs = []
test_indexes = []

random.seed()

folder = '../data/TFRecord/'
n_recordings = 10
n_experiment_iterations = n_recordings

signal_file_names = [folder + 'e_mix33_n' + str(noise_level) + '_iter' + str(i) + '.tfrecord' \
                     for i in range(10) ]

    
for experiment_iteration_index in range(n_experiment_iterations):
    
    print("======= Iteration ", (experiment_iteration_index + 1), "=======")
    
    ###########################################################################
    ### DATA LOADING 
    ###########################################################################
    
    test_dataset_filenames = [signal_file_names[experiment_iteration_index]]
    train_dataset_filenames = list(set(test_dataset_filenames).symmetric_difference(signal_file_names))
    
    print("Train on: ")
    for fname in train_dataset_filenames:
        print(fname)
    print("Test on: ", test_dataset_filenames)
    
    shuffle(train_dataset_filenames)
    
    train_dataset = tf.data.TFRecordDataset(train_dataset_filenames)
    train_dataset = train_dataset.shard(num_shards = 1, index = 0)
    train_dataset = train_dataset.map(_parse_function) 
    
    # train_dataset = train_dataset.cache()
    train_dataset = train_dataset.shuffle(buffer_size = 2000, #4000
                                          reshuffle_each_iteration= True)
    train_dataset = train_dataset.batch(batch_size)
    
    # Create Test dataset
    test_dataset = tf.data.TFRecordDataset(test_dataset_filenames )
    test_dataset = test_dataset.map(_parse_function)    
    
    # Generate batches
    test_dataset = test_dataset.batch(batch_size)
    
    ###########################################################################
    ### NETWORK TRAINING
    ###########################################################################
    
    input_shape = (512 , 4)
    lr = .001
    epochs = 50
    activation_function = 'elu'
    kernel_initializer = 'glorot_uniform'
    
    denoising_ae_model = create_fcdae(input_shape, activation_function, \
                                      kernel_initializer, lr)
   
    history = denoising_ae_model.fit(
        train_dataset,
        batch_size = batch_size,
        epochs = epochs,
        validation_data= test_dataset,
        verbose = 0
    )
    
    ###########################################################################
    ### NETWORK VALIDATION
    ###########################################################################
    
    predictions = denoising_ae_model.predict(test_dataset)
    
    testy = []
    testX = []
    for X, y in test_dataset:
        for i in range(y.shape[0]):
            tmpy = y[i].numpy()
            testy.append(tmpy)
            testX.append(X[i, :].numpy())
            
    testy = np.asarray(testy)
    testX = np.concatenate(testX, axis = 0) 
    
    predictions = np.reshape(predictions, (predictions.shape[0] * predictions.shape[1], predictions.shape[2]))
    testy = np.reshape(testy, (testy.shape[0] * testy.shape[1], testy.shape[2]))
    
    # Uncomment the following to save the model's output
    #clean_signal_output_filename = '../data/fcdae_output/e_mix33_n' \
    #    + str(noise_level) + '_iter' + str(experiment_iteration_index) + '_cdae.mat'
    #mdict = {'testX': testX, 'testy':testy, 'predictions':predictions}
    #sio.savemat(clean_signal_output_filename, mdict)

    
    SNR_before, SNR_after, SNR_imp = calculateSNRImprovement(testX = testX,
                                                             testy = testy,
                                                             predictions = predictions)
    RMSE = calculateRMSE(testy, predictions)
        
    SNRs.append({'SNR_before': SNR_before, 'SNR_after': SNR_after, 'SNR_imp': SNR_imp})
    RMSEs.append(RMSE)
    test_indexes.append(test_dataset_filenames)
    
    for i in range(SNR_imp.size):
        SNR_after_str = "{:.2f}".format(SNR_after[i])
        SNR_before_str = "{:.2f}".format(SNR_before[i])
        SNR_imp_str = "{:.2f}".format(SNR_imp[i])
        print("Channel ", i, "SNR after:  ",SNR_after_str," SNR improvement: ", SNR_imp_str, \
              " dB | Before: ", SNR_before_str, " dB | RMSE: ", RMSE[i])

mean_SNR_improvement = 0
mean_SNR_before = 0
mean_RMSE = 0
for i in range(len(SNRs)):
    mean_SNR_improvement += SNRs[i]['SNR_imp']
    mean_SNR_before += SNRs[i]['SNR_before']
    mean_RMSE += RMSEs[i]
    
mean_SNR_improvement /= float(len(SNRs))
mean_SNR_before /= float(len(SNRs))
mean_RMSE /= float(len(RMSEs))

print("=== Mean SNRs before ===")
print(mean_SNR_before)
print("=== Mean SNRs improvement ===")
print(mean_SNR_improvement)
print("=== Mean RMSEs improvement ===")
print(mean_RMSE)