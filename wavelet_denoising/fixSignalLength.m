function y = fixSignalLength(x, N)
% Removes a small number of samples from the end of the signal, so that
% the total signal length is divisible by 2^N
    x_len = size(x, 1);
    new_len = fix(x_len/2^N) * 2^N;
    y = x(1:new_len, :);
end
