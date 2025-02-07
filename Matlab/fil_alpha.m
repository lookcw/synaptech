function Hd = fil_alpha
%FIL_ALPHA Returns a discrete-time filter object.

% MATLAB Code
% Generated by MATLAB(R) 9.2 and the DSP System Toolbox 9.4.
% Generated on: 16-Jun-2017 10:25:35

% Equiripple Bandpass filter designed using the FIRPM function.

% All frequency values are in Hz.
Fs = 250;  % Sampling Frequency

Fstop1 = 7.6;             % First Stopband Frequency
Fpass1 = 8.2;             % First Passband Frequency
Fpass2 = 11.8;            % Second Passband Frequency
Fstop2 = 12.4;            % Second Stopband Frequency
Dstop1 = 0.01;            % First Stopband Attenuation
Dpass  = 0.057501127785;  % Passband Ripple
Dstop2 = 0.01;            % Second Stopband Attenuation
dens   = 20;              % Density Factor

% Calculate the order from the parameters using FIRPMORD.
[N, Fo, Ao, W] = firpmord([Fstop1 Fpass1 Fpass2 Fstop2]/(Fs/2), [0 1 ...
                          0], [Dstop1 Dpass Dstop2]);

% Calculate the coefficients using the FIRPM function.
b  = firpm(N, Fo, Ao, W, {dens});
Hd = dfilt.dffir(b);

% [EOF]
