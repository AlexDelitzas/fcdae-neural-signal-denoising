function xd = wden_swt(X, TPTR, SORH, SCAL, N, WNAME)
% Implements signal denoising with the Stationary Wavelet Transform (SWT)

    swc = swt(X, N, WNAME);
    
    swcnew = swc;
    ThreshML = wthrmngr('sw1ddenoLVL', TPTR, swc, SCAL);
    
    for jj = 1:N
        swcnew(jj,:) = wthresh(swc(jj, :), SORH, ThreshML(jj));
    end
    
    xd = iswt(swcnew, WNAME);
end