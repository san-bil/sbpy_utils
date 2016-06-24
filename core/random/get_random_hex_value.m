function out = get_random_hex_value(hex_length)

% in: length of hex value desired
%
% out: random hex value
%
% desc: returns a random hex value
%
% tags: #hex #random #sample

if(~exist('length','var'))
    hex_length=5;
end
    
    
out = randsample('0123456789abcdef',hex_length,true);
