# -*- coding: utf-8 -*-
from tensorflow.keras.layers import Conv1D, Conv1DTranspose
from tensorflow.keras.models import Sequential
import tensorflow as tf


def create_fcdae(input_shape, activation_function, kernel_initializer, lr):
    autoencoder_model = Sequential()
    
    kernel_size = 3
    n_layers = 5
    
    # encoder part
    autoencoder_model.add(Conv1D(32, kernel_size = kernel_size ,input_shape = input_shape, strides = 1, padding = 'same', 
                                        activation = activation_function,  
                                        kernel_initializer = kernel_initializer))
    
    for i in range(1, n_layers):
      autoencoder_model.add(Conv1D(2**(i + 5), kernel_size = kernel_size, strides = 2, padding = 'same', 
                                          activation = activation_function,
                                          kernel_initializer = kernel_initializer))
    
    # decoder part
    for i in range(n_layers - 2, -1, -1):
      autoencoder_model.add(Conv1DTranspose(2**(i + 5) , kernel_size = kernel_size, strides = 2, padding = 'same',  
                              activation = activation_function,  
                              kernel_initializer = kernel_initializer
                              ))
    
    
    autoencoder_model.add(Conv1DTranspose(4 , kernel_size = kernel_size, strides = 1, padding = 'same',  
                              activation = 'linear',  
                              kernel_initializer = kernel_initializer
                              ))
    

    opt = tf.keras.optimizers.Adam(learning_rate = lr)
    autoencoder_model.compile(optimizer=opt, loss= 'mse')

    return autoencoder_model
