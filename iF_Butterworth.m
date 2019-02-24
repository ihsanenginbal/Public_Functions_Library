% Function of bandpass Butterworth filter
% Senso Engineering Ltd
% v1.0 : June 2017



function filtered_data=iF_Butterworth(order,lowFreq,hiFreq,dt,data)

fs=1/dt;
[b,a]=butter(order, [lowFreq hiFreq]/(fs/2), 'bandpass');
filtered_data=filter(b,a,data);