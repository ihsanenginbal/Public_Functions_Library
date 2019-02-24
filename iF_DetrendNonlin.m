%% iMatlab Personal Library
% Detrending with a nonlinear function
% It removes a nonlinear trend from a vactor of raw data
% by using least-squares polynomial fit.
% i.e.bal@pl.hanze.nl
% v2.0, June 2018

% OUTPUT
% detrended_data   : The processed data after removing detrend

% INPUT
% raw_data : Raw data


function detrended_data = iF_DetrendNonlin(raw_data, varargin)

if numel(varargin)>=1
    order = varargin{1};
else
    order = 2;
end

p = polyfit((1:numel(x))', x(:), order);
y = x(:) - polyval(p, (1:numel(x))');

end
