


% DETRENDNONLIN Remove a non-linear trend from a vector
% The nonlinearity is removed by subtracting a least-squares
% polynomial fit.
%
% Y = DETRENDNONLIN(X) subtracts a second order polynomial fit from
% the data vector X.
%
% Y = DETRENDNONLIN(X, n) subtracts a polynomial fit of order n from
% the data vector X.
%Senso Engineering Ltd
% v1.1

function y = iF_detrendnonlin(x, varargin)

if numel(varargin)>=1
    order = varargin{1};
else
    order = 2;
end

p = polyfit((1:numel(x))', x(:), order);
y = x(:) - polyval(p, (1:numel(x))');

end