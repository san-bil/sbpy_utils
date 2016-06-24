function out=kv_create_w_names(varargin)

% in: variables that you want to be stored in an associative-array/map/dictionary
%
% out: a 2 column cell-array, where the left column is a string key (set to the variable name passed in), and the right column is the variable value
%
% desc: as above.
%
% tags: #map #dictionary #associativearray #associative #keyvalue


if(mod(length(varargin),2)~=0)
    error('non-matching number of keys and values')
end

out = {};

for i = 1:floor(length(varargin)/2)
    idx=((i-1)*2)+1;
    var_name = varargin{idx};
    var_val = varargin{idx+1};
    out = [out;{var_name,var_val}];
    
end

end
