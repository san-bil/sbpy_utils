function out=kv_magic_set(in,map)

% in: variables that you want to be stored in an associative-array/map/dictionary
%
% out: a 2 column cell-array, where the left column is a string key (set to the variable name passed in), and the right column is the variable value
%
% desc: as above.
%
% tags: #map #dictionary #associativearray #associative #keyvalue

var_name = inputname(in);
out = kv_set(var_name,in,map);