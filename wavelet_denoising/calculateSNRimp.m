function snr_imp = calculateSNRimp(x_noisy, x_denoised, x_clean, n_channels)
% Calculates the SNR improvement
    snr_imp = zeros(n_channels, 1);
    
    for l=1:n_channels
        num = sum((x_noisy(:, l) - x_clean).^2);
        denom = sum((x_denoised(:, l) - x_clean).^2);
        
        snr_imp(l) = 10*log10(num / denom);
    end
end