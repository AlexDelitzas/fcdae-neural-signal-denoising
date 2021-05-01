% 
% Description: This script evaluates the performance of the Stationary Wavelet 
% Transform (SWT) for denoising Extracellular Action Potential recordings
%

clear;
close all;

%% INITIALIZATION

data_path = '../data/mat/';
out_data_path = '../out_data_swt/';
noise_selection = 'n7';
n_folds = 10;

% set the parameter space
TPTR_settings = {'sqtwolog', 'heursure', 'rigrsure', 'minimaxi'};
SORH_settings = {'s', 'h'};
SCAL_settings = {'mln'};
N_settings = {4, 5};
WNAME_settings = {'haar', 'coif2', 'db4', 'bior6.8', 'sym7'};

%% READ DATA

noisy_signals = cell(n_folds, 1);
gt_signals = cell(n_folds, 1);

for i=1:n_folds
    data_filename = strcat(data_path, 'e_mix33_', noise_selection, '_iter', ...
        num2str(i-1), '.mat');
    
    [noisy_signals{i}, gt_signals{i}, n_channels] = loadData(data_filename);
    
    noisy_signals{i} = double(fixSignalLength(noisy_signals{i}, max([N_settings{:}])));
    gt_signals{i} = double(fixSignalLength(gt_signals{i}, max([N_settings{:}])));
end

%% PARAMETER TUNING AND PERFORMANCE EVALUATION

param_comb = combvec(1:length(TPTR_settings), 1:length(SORH_settings), ...
    1:length(SCAL_settings), 1:length(N_settings), 1:length(WNAME_settings));

param_comb_size = size(param_comb, 2);

fprintf('** SWT DENOISING ** \n\n')
fprintf('Parameter space size: %d', param_comb_size)

snr_imp = zeros(n_folds, n_channels);
rmse = zeros(n_folds, n_channels);

for i=1:n_folds
    
    fprintf('\n\n========== PROGRESS %d/%d ==========\n', i, n_folds);
    
    test_idx = i;
    
    % create training set
    if test_idx == 1
        noisy_train_signal = noisy_signals{2};
        gt_train_signal = gt_signals{2};
        j_s = 3;
    else
        noisy_train_signal = noisy_signals{1};
        gt_train_signal = gt_signals{1};
        j_s = 2;
    end
    
    for j=j_s:n_folds
        if j == test_idx
            continue
        end
        noisy_train_signal = cat(1, noisy_train_signal, noisy_signals{j});
        gt_train_signal = cat(1, gt_train_signal, gt_signals{j});
    end
    
    % create test set
    noisy_test_signal = noisy_signals{test_idx};
    gt_test_signal = gt_signals{test_idx};
    
    % TRAINING
    objFunctionValues = zeros(param_comb_size, 1);
    
    for iter=1:param_comb_size
        TPTR = TPTR_settings{param_comb(1, iter)};
        SORH = SORH_settings{param_comb(2, iter)};
        SCAL = SCAL_settings{param_comb(3, iter)};
        N = N_settings{param_comb(4, iter)};
        WNAME = WNAME_settings{param_comb(5, iter)};

        filtered_train_signal = zeros(size(noisy_train_signal));

        mse = 0;
        for l=1:n_channels  
            X = noisy_train_signal(:, l);
            filtered_train_signal(:, l) = wden_swt(X, TPTR, SORH, SCAL, N, WNAME);

            mse = mse + immse(filtered_train_signal(:, l), gt_train_signal);
        end

        objFunctionValues(iter) = mse / n_channels;
    end
    
    [min_mse, pos] = min(objFunctionValues);
    best_params = param_comb(:, pos);
    fprintf('[*] Minimum MSE: %.6f', min_mse)
    
    % TESTING
    TPTR = TPTR_settings{best_params(1)};
    SORH = SORH_settings{best_params(2)};
    SCAL = SCAL_settings{best_params(3)};
    N = N_settings{best_params(4)};
    WNAME = WNAME_settings{best_params(5)};
    
    filtered_test_signal = zeros(size(noisy_test_signal));

    for l=1:n_channels  
        X = noisy_test_signal(:, l);
        filtered_test_signal(:, l) = wden_swt(X, TPTR, SORH, SCAL, N, WNAME);
        
        % calculate RMSE
        rmse(i, l) = sqrt(immse(filtered_test_signal(:, l), gt_test_signal));
    end

    snr_imp(i, 1:n_channels) = calculateSNRimp(noisy_test_signal, filtered_test_signal, gt_test_signal, n_channels)';
    
    % save output
%     best_settings = {TPTR, SORH, SCAL, N, WNAME};
%     out_filename = strcat(out_data_path, 'e_mix33_', noise_selection, '_iter', ...
%         num2str(i-1), '_filtered', '.mat');
%     save(out_filename, 'filtered_test_signal', 'best_settings');
    
    clear noisy_train_signal gt_train_signal filtered_train_signal ...
        noisy_test_signal gt_test_signal filtered_test_signal best_params
        
end

total_snr_imp = mean(snr_imp, 1);
total_rmse = mean(rmse, 1);

fprintf('\n\nPer channel SNR improvement: [')
fprintf('%g, ', total_snr_imp(1:end-1));
fprintf('%g]\n', total_snr_imp(end));

fprintf('\nPer channel RMSE: [')
fprintf('%g, ', total_rmse(1:end-1));
fprintf('%g]\n\n', total_rmse(end));

