function dict=kv_save(mat_file,varargin)

% in: variables that you want to be stored in an associative-array/map/dictionary
%
% out: a 2 column cell-array, where the left column is a string key (set to the variable name passed in), and the right column is the variable value
%
% desc: as above.
%
% tags: #map #dictionary #associativearray #associative #keyvalue

dict = {};

for i = 1:length(varargin)

    var_name = inputname(i);
    var_val = varargin{i};
    dict = [dict;{var_name,var_val}];
    
end

save(mat_file,'dict');


