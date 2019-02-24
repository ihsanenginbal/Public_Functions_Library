%% iMatlab Personal Library
% Butterworth signal filter
% Author: Prof. Ihsan Engin BAL
% Hanze University of Applied Sciences, Groningen, Netherlands
% www.eqresearch.nl
% i.e.bal@pl.hanze.nl
% v4.0, September 2018

% OUTPUT
% filtered data  : Data after filtering

% INPUT
% order : n^th order of the filtering operation 
% lowFreq : low frequency of filtering
% hiFreq : high frequency of filtering
% dt : delta-t in sec
% data : raw data



function filtered_data=iF_Butterworth(order,lowFreq,hiFreq,dt,data)

fs=1/dt;
[b,a]=butter(order, [lowFreq hiFreq]/(fs/2), 'bandpass');
filtered_data=filter(b,a,data);
