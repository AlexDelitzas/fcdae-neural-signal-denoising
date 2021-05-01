function [noisy_signal, gt_signal, n_channels] = loadData(fileName)
% Loads the .mat data 
    x = load(fileName);
    noisy_signal = x.y;
    gt_signal = x.ground_truth';
    n_channels = size(noisy_signal, 2);
end