Code for the paper "Removing Noise from Extracellular Neural Recordings Using Fully Convolutional Denoising Autoencoders"
<br />

Paper: https://ieeexplore.ieee.org/abstract/document/9630585

Cite as:

```
@INPROCEEDINGS{9630585,  
  author={Kechris, Christodoulos and Delitzas, Alexandros and Matsoukas, Vasileios and Petrantonakis, Panagiotis C.},  
  booktitle={2021 43rd Annual International Conference of the IEEE Engineering in Medicine \& Biology Society (EMBC)},   
  title={Removing Noise from Extracellular Neural Recordings Using Fully Convolutional Denoising Autoencoders},   
  year={2021},  
  volume={},  
  number={},  
  pages={890-893},  
  doi={10.1109/EMBC46164.2021.9630585}
}
```

## Abstract

Extracellular recordings are severely contaminated by a considerable amount of noise sources, rendering the denoising process an extremely challenging task that should be tackled for efficient spike sorting. To this end, we propose an end-to-end deep learning approach to the problem, utilizing a Fully Convolutional Denoising Autoencoder, which learns to produce a clean neuronal activity signal from a noisy multichannel input. The experimental results on simulated data show that our proposed method can improve significantly the quality of noise-corrupted neural signals, outperforming widely-used wavelet denoising techniques.

<br />

## Requirements

* Python (tested with v3.8): Used for the data generation and the network's development

* Matlab (tested with R2020b): Used for the development of the wavelet denoising methods to compare the network's performance

In order to install the necessary Python libraries, run the following command:

```
pip install -r requirements.txt
```

*Note*: To run the dataset generation scripts, you should also install the MEArec Python library. Instructions can be found [here](https://mearec.readthedocs.io/en/latest/installation.html).

<br />

## Dataset 

The extracellular recordings that were used for training and evaluation are available in two formats, i.e. `.mat` and `.tfrecord`.

```
.
|-- data/
|   |-- mat/
|   |-- TFRecord/
.
```

Data are organized as follows:

```
e_mix33_n<L>_iter<K>.{mat,tfrecord}
```

where 

* `<L>` is the noise level in μV (`<L>` = [7, 9, 15, 20]) and 
* `<K>` is the recording number (`<K>` = [0, 1, ..., 9])

<br />

## How to run

### Fully Convolutional Denoising Autoencoder

```
cd fcdae_network
```

For **Training & Evaluation**:

Run

```
python fc_dae_model_train_and_test.py
```

<br />

### Wavelet denoising methods DWT and SWT

```
cd wavelet_denoising
```

For: 
* Discrete Wavelet Transform (DWT): Run `dwt_denoising.m`
* Stationary Wavelet Transform (SWT): Run `swt_denoising.m`

<br />

### Data generation

In case you want to recreate a dataset, follow the instructions below:

```
cd data_generation
```

*Step 1 (Optional)*: Run the following command to generate the extracellular templates

```
python generate_templates.py
```

The templates will be saved in the folder `data_generation/templates/` in `.h5` format. Step 1 can be completely omitted by using the existing templates located in the aforementioned folder.

*Step 2*: Run the following command to create the extracellular recordings

```
python generate_recordings.py
```

The recordings will be saved in the folder `data/mat/` in `.mat` format and in the folder `data_generation/h5_recordings/` in `.h5` format. In case you want to alter the generation settings of the recordings, you can change the parameters in the `.yaml` files located at `data_generation/recording_settings/`.

*Step 3*: Run the following command to convert the extracellular recordings data in `.tfrecord` format.

```
python generate_tfrecords.py
```

After the conversion, the recordings will be saved in the folder `data/TFRecord/` in `.tfrecord` format. These files are used for the autoencoder's training.


<br />

## Results

### Per channel SNR Improvement

<br />

<table>
<thead>
<tr>
<th align="center" colspan="5">Fully Convolutional Denoising Autoencoder (FCDAE)</th>
</tr>
<tr>
<th align="center">Input Noise Level (μV / (mindB,maxdB))</th>
<th align="center">SNR Improvement CH1 (dB)</th>
<th align="center">SNR Improvement CH2 (dB)</th>
<th align="center">SNR Improvement CH3 (dB)</th>
<th align="center">SNR Improvement CH4 (dB)</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">7 / (0.60, 2.87)</td>
<td align="center">8.184</td>
<td align="center">7.672</td>
<td align="center">6.207</td>
<td align="center">8.429</td>
</tr>
<tr>
<td align="center">9 / (-1.36, 0.77)</td>
<td align="center">10.012</td>
<td align="center">7.901</td>
<td align="center">7.241</td>
<td align="center">9.455</td>
</tr>
<tr>
<td align="center">15 / (-5.29, -3.59)</td>
<td align="center">9.997</td>
<td align="center">9.888</td>
<td align="center">9.506</td>
<td align="center">11.223</td>
</tr>
<tr>
<td align="center">20 / (-7.02, -5.97)</td>
<td align="center">10.579</td>
<td align="center">10.460</td>
<td align="center">11.029</td>
<td align="center">11.499</td>
</tr>
</tbody>
</table>

<br />

<table>
<thead>
<tr>
<th align="center" colspan="5">Discrete Wavelet Transform (DWT)</th>
</tr>
<tr>
<th align="center">Input Noise Level (μV / (mindB,maxdB))</th>
<th align="center">SNR Improvement CH1 (dB)</th>
<th align="center">SNR Improvement CH2 (dB)</th>
<th align="center">SNR Improvement CH3 (dB)</th>
<th align="center">SNR Improvement CH4 (dB)</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">7 / (0.60, 2.87)</td>
<td align="center">1.898</td>
<td align="center">4.095</td>
<td align="center">2.866</td>
<td align="center">3.061</td>
</tr>
<tr>
<td align="center">9 / (-1.36, 0.77)</td>
<td align="center">4.105</td>
<td align="center">4.117</td>
<td align="center">3.424</td>
<td align="center">3.757</td>
</tr>
<tr>
<td align="center">15 / (-5.29, -3.59)</td>
<td align="center">5.970</td>
<td align="center">6.675</td>
<td align="center">6.016</td>
<td align="center">6.422</td>
</tr>
<tr>
<td align="center">20 / (-7.02, -5.97)</td>
<td align="center">6.963</td>
<td align="center">6.961</td>
<td align="center">7.104</td>
<td align="center">7.285</td>
</tr>
</tbody>
</table>

<br />

<table>
<thead>
<tr>
<th align="center" colspan="5">Stationary Wavelet Transform (SWT)</th>
</tr>
<tr>
<th align="center">Input Noise Level (μV / (mindB,maxdB))</th>
<th align="center">SNR Improvement CH1 (dB)</th>
<th align="center">SNR Improvement CH2 (dB)</th>
<th align="center">SNR Improvement CH3 (dB)</th>
<th align="center">SNR Improvement CH4 (dB)</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">7 / (0.60, 2.87)</td>
<td align="center">1.899</td>
<td align="center">4.557</td>
<td align="center">3.380</td>
<td align="center">3.219</td>
</tr>
<tr>
<td align="center">9 / (-1.36, 0.77)</td>
<td align="center">3.680</td>
<td align="center">4.021</td>
<td align="center">3.649</td>
<td align="center">3.692</td>
</tr>
<tr>
<td align="center">15 / (-5.29, -3.59)</td>
<td align="center">6.415</td>
<td align="center">7.503</td>
<td align="center">6.770</td>
<td align="center">6.946</td>
</tr>
<tr>
<td align="center">20 / (-7.02, -5.97)</td>
<td align="center">7.569</td>
<td align="center">7.627</td>
<td align="center">7.673</td>
<td align="center">7.836</td>
</tr>
</tbody>
</table>

<br />

### Per channel RMSE

<br />

<p>
<table>
<thead>
<tr>
<th align="center" colspan="5">Fully Convolutional Denoising Autoencoder (FCDAE)</th>
</tr>
<tr>
<th align="center">Input Noise Level (μV / (mindB,maxdB))</th>
<th align="center">RMSE CH1</th>
<th align="center">RMSE CH2</th>
<th align="center">RMSE CH3</th>
<th align="center">RMSE CH4</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">7 / (0.60, 2.87)</td>
<td align="center">0.02321</td>
<td align="center">0.02344</td>
<td align="center">0.02341</td>
<td align="center">0.02363</td>
</tr>
<tr>
<td align="center">9 / (-1.36, 0.77)</td>
<td align="center">0.02339</td>
<td align="center">0.02332</td>
<td align="center">0.02342</td>
<td align="center">0.02342</td>
</tr>
<tr>
<td align="center">15 / (-5.29, -3.59)</td>
<td align="center">0.03237</td>
<td align="center">0.03233</td>
<td align="center">0.03240</td>
<td align="center">0.03235</td>
</tr>
<tr>
<td align="center">20 / (-7.02, -5.97)</td>
<td align="center">0.03673</td>
<td align="center">0.03664</td>
<td align="center">0.03662</td>
<td align="center">0.03667</td>
</tr>
</tbody>
</table>
</p>
<br />

<table>
<thead>
<tr>
<th align="center" colspan="5">Discrete Wavelet Transform (DWT)</th>
</tr>
<tr>
<th align="center">Input Noise Level (μV / (mindB,maxdB))</th>
<th align="center">RMSE CH1</th>
<th align="center">RMSE CH2</th>
<th align="center">RMSE CH3</th>
<th align="center">RMSE CH4</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">7 / (0.60, 2.87)</td>
<td align="center">0.04727</td>
<td align="center">0.03507</td>
<td align="center">0.03402</td>
<td align="center">0.04321</td>
</tr>
<tr>
<td align="center">9 / (-1.36, 0.77)</td>
<td align="center">0.04649</td>
<td align="center">0.03689</td>
<td align="center">0.03657</td>
<td align="center">0.04553</td>
</tr>
<tr>
<td align="center">15 / (-5.29, -3.59)</td>
<td align="center">0.05209</td>
<td align="center">0.04758</td>
<td align="center">0.04767</td>
<td align="center">0.05496</td>
</tr>
<tr>
<td align="center">20 / (-7.02, -5.97)</td>
<td align="center">0.05535</td>
<td align="center">0.05442</td>
<td align="center">0.05636</td>
<td align="center">0.05825</td>
</tr>
</tbody>
</table>

<br />

<table>
<thead>
<tr>
<th align="center" colspan="5">Stationary Wavelet Transform (SWT)</th>
</tr>
<tr>
<th align="center">Input Noise Level (μV / (mindB,maxdB))</th>
<th align="center">RMSE CH1</th>
<th align="center">RMSE CH2</th>
<th align="center">RMSE CH3</th>
<th align="center">RMSE CH4</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">7 / (0.60, 2.87)</td>
<td align="center">0.04731</td>
<td align="center">0.03344</td>
<td align="center">0.03221</td>
<td align="center">0.04279</td>
</tr>
<tr>
<td align="center">9 / (-1.36, 0.77)</td>
<td align="center">0.04891</td>
<td align="center">0.03823</td>
<td align="center">0.03608</td>
<td align="center">0.04638</td>
</tr>
<tr>
<td align="center">15 / (-5.29, -3.59)</td>
<td align="center">0.04998</td>
<td align="center">0.04389</td>
<td align="center">0.04393</td>
<td align="center">0.05199</td>
</tr>
<tr>
<td align="center">20 / (-7.02, -5.97)</td>
<td align="center">0.05209</td>
<td align="center">0.05092</td>
<td align="center">0.05312</td>
<td align="center">0.05500</td>
</tr>
</tbody>
</table>

<br />
