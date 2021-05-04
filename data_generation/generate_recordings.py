# -*- coding: utf-8 -*-
import MEArec as mr
import yaml
import h5py
import numpy as np
import scipy.io as sio 

noise = 7
n_iterations = 10
experiment_name = 'e_mix33_n' + str(noise)
argument_file = './recording_settings/' + experiment_name + '.yaml'

cur_iter = 0

spiketrain_seeds = []
template_seeds = []
convolution_seeds = []
noise_seeds = []

while cur_iter < n_iterations:

  recordings_params = mr.get_default_recordings_params()

  recording_path = './h5_recordings/' + experiment_name + '_iter' + str(cur_iter) + '.h5'
  mat_output_filename = '../data/mat/' + experiment_name + '_iter' + str(cur_iter) + '.mat'

  print("Reading settings from input file " + argument_file)
  print('Generated recordings saved in file ' + recording_path)
  print('\n\n===================================\n')

  with open(argument_file) as f:
    argument_data = yaml.load(f)

    print("Read arguments: \n")
    for argument in argument_data:
      print(argument + " : " + str(argument_data[argument]))

    template_output_file = argument_data['template_file']

    # recording duration (in seconds)
    recordings_params['spiketrains']['duration'] = argument_data['duration'] 

    # number of excitatory cells
    recordings_params['spiketrains']['n_exc'] = argument_data['n_exc']
    # number of inhibitatory cells
    recordings_params['spiketrains']['n_inh'] = argument_data['n_inh']

    # sampling frequency (Hz)
    recordings_params['recordings']['fs'] = 10000
    #noise mode
    recordings_params['recordings']['noise_level'] = argument_data['noise_level']
    recordings_params['recordings']['noise_mode'] = argument_data['noise_mode']
    #use noise color
    recordings_params['recordings']['noise_color'] = True

    # enable burstnig
    recordings_params['recordings']['bursting'] = argument_data['bursting']

    # apply band pass filtering
    recordings_params['recordings']['filter'] = False

    recordings_params['recordings']['drifting'] = False

    recordings_params['recordings']['overlap'] = argument_data['overlap']

  print('\n\n===================================\n\n')
  print("Generating recordings")

  try:
    recordings_params['seeds']['spiketrains'] = np.random.randint(1, 10000)
    recordings_params['seeds']['templates'] = np.random.randint(1, 10000)
    recordings_params['seeds']['convolution'] = np.random.randint(1, 10000)
    recordings_params['seeds']['noise'] = np.random.randint(1, 10000)

    while (recordings_params['seeds']['spiketrains'] in spiketrain_seeds or \
        recordings_params['seeds']['templates'] in template_seeds or\
        recordings_params['seeds']['convolution'] in convolution_seeds or \
        recordings_params['seeds']['noise'] in noise_seeds):

      recordings_params['seeds']['spiketrains'] = np.random.randint(1, 10000)
      recordings_params['seeds']['templates'] = np.random.randint(1, 10000)
      recordings_params['seeds']['convolution'] = np.random.randint(1, 10000)
      recordings_params['seeds']['noise'] = np.random.randint(1, 10000)

    recgen = mr.gen_recordings(params = recordings_params, templates = template_output_file)
    
    spiketrain_seeds.append(recordings_params['seeds']['spiketrains'])
    template_seeds.append(recordings_params['seeds']['templates'])
    convolution_seeds.append(recordings_params['seeds']['convolution'])
    noise_seeds.append(recordings_params['seeds']['noise'])

    mr.save_recording_generator(recgen, recording_path)

    # Save to .mat format
    with h5py.File(recording_path, 'r') as f:
      y = f['recordings'][()]
      gt = f['spike_traces'][()]
      
      gt[:, 0] = gt[:, 0] - gt[:, 0].mean()
      ground_truth = gt[:, 0] 
      for i in range(1, gt.shape[1]):
          gt[:, i] = gt[:, i] - gt[:, i].mean()
          ground_truth += gt[:, i] 
      ground_truth /= np.abs(ground_truth).max()
      
      mdict = {'y': y, 'ground_truth':ground_truth}

      sio.savemat(mat_output_filename, mdict)
      cur_iter += 1
  except RuntimeError:
    pass

print("Done.")