Code for the paper [TODO]
<br />

## Abstract

Extracellular recordings are severely contaminated by a considerable amount of noise sources, rendering the denoising process an extremely challenging task that should be tackled for efficient spike sorting. To this end, we propose an end-to-end deep learning approach to the problem, utilizing a Fully Convolutional Denoising Autoencoder, which learns to produce a clean neuronal activity signal from a noisy multichannel input. The experimental results on simulated data show that our proposed method can improve significantly the quality of noise-corrupted neural signals, outperforming widely-used wavelet denoising techniques.

## Requirements

* Python (tested with v3.8): Used for the data generation and the network's development

* Matlab (tested with R2020b): Used for the development of the wavelet denoising methods to compare the network's performance

In order to install the necessary Python libraries, run the following command:

```
TODO
```

## How to run

### Data generation

### Fully Convolutional Denoising Autoencoder

```
cd fcdae_network
```

**Training & Evaluation**

Run:

```
python fc_dae_model_train_and_test.py
```

### Wavelet denoising methods DWT and SWT

```
cd wavelet_denoising
```

For: 
* Discrete Wavelet Transform (DWT): Run `dwt_denoising.m`
* Stationary Wavelet Transform (SWT): Run `swt_denoising.m`

## Results

### Per channel SNR Improvement

<br />

<table>
<thead>
<tr>
<th align="center" colspan="5">Fully Convolutional Denoising Autoencoder (FCDAE)</th>
</tr>
<tr>
<th align="center">Input Noise Level (μV / (mindB,maxdB)</th>
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
<th align="center">Input Noise Level (μV / (mindB,maxdB)</th>
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
<th align="center">Input Noise Level (μV / (mindB,maxdB)</th>
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

[TODO]
