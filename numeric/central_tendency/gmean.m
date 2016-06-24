function y = gmean(x,k)
%GMEAN Generalized mean.
% A generalized mean, also known as power mean, Holder mean or Kolmogorov-
% Negumo function of the mean, is an abstraction of the Pythagorean means
% included harmonic, geometric, and arithmetic mean.
% It is defined as,
%
%              Mk = [1/n(x1^k + x2^k + ... + xn^k)]^1/k
%
% where: k is indicator power for the desired mean (-1 = harmonic mean;
% 0 = geometric mean; 1 = arithmetic mean;2 = root mean square).
% Although it is not possible to put k = 0 directly but, according to the
% L’Hopital’s theorem,  the limit as k tends to zero exists,
%
%              Mk = lim k->0 [1/n(x1^k + x2^k + ... + xn^k)]^1/k
%                 = (x1x2 ... xn)^1/k
%
% Syntax: function y = gmean(x)
%
% Input:
%    x - Input data vector
%    k - desired power (-1 = harmonic mean ;0 = geometric mean;
%        1 = arithmetic mean;2 = root mean square)
% Output:
%    y - Desired mean
%
% Example 1. Suppose you have this beach monitoring data from different
% dates. Data of Enterococci bacteria per 100 milliliters of 4 samples are:
% 6, 50, 9, 1200
%
% Data vector is:
%    x = [6,5,9,1200];
%
% Calling on Matlab the function: 
%    gmean(x,0)
%
% Answer is:
% Geometric mean
%
%    ans = 42.4264
%
% Example 2. We are interested to evaluate the percent change in a population
% from 3 samples which give +12%, -8%, and +2%. 
%
% Data vector is:
%    x = [1.12,0.92,1.02];
%
% Calling on Matlab the function: 
%    y = gmean(x,0)
%
% Answer is:
% Geometric mean
%
%    y = 1.0167
%
% *NOTE: Subtracting 1 from this value gives the geometric mean of +1.67% as
%        a net rate of population growth
%
% Example 3. We need to calculate the average of the next 5 rates:1,2,3,4,5.
%
% Data vector is:
%    x = [1,2,3,4,5];
%
% Calling on Matlab the function: 
%    gmean(x,-1)
%
% Answer is:
% Harmonic mean
%
% ans = 2.1898
%
% Created by A. Trujillo-Ortiz, R. Hernandez-Walls and K. Barba-Rojo
%            Facultad de Ciencias Marinas
%            Universidad Autonoma de Baja California
%            Apdo. Postal 453
%            Ensenada, Baja California
%            Mexico.
%            atrujo@uabc.mx
%
% Copyright. April 01, 2008.
%
% To cite this file, this would be an appropriate format:
% Trujillo-Ortiz, A., R. Hernandez-Walls and K. Barba-Rojo. (2008). 
% gmean: Generalized mean. A MATLAB file. [WWW document]. URL
% http://www.mathworks.com/matlabcentral/fileexchange/loadFile.do?objectId=19469
%
% References:
% Phillips, G. M. (2000), Two Millennia of Mathematics: From Archimedes to
%     Gauss. Springer-Verlag:New York, 240 pp 
% Sheldon, N. (2004), The Generalized Mean. Teaching Statistics,
%     26(1):24-25
% 

error(nargchk(1,2,nargin));

n  = length(x);

if (k == -1) | (k == 1) | (k == 2),
    xk = x.^k;
    y = (sum(xk)/n)^(1/k);
    if (k == -1),
        disp('Harmonic mean');
    elseif (k == 1),
        disp('Arithmetic mean');
    else (k == 2),
        disp('Root mean square');
    end
elseif (k == 0),
    lx = log(x);
    y = exp(sum(lx)/n);
    disp('Geometric mean');
else
    ('Other power does not have any significance.')
end

return,