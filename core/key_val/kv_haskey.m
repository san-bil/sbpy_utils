function [ my_flag ] = kv_haskey( key,options )


% in: a string key, a 2-column cell array representing a dictionary (first column==string keys, second column==values), 
%
% out: a boolean representing whether the input key is in the dictionary or not.
%
% desc: as above.
%
% tags: #map #dictionary #associativearray #associative #keyvalue

if(iscell(key))
    error('kv_get: Key must be a string or double type.')
end

my_flag = 0;
for i=1:size(options,1)
    if((ischar(options{i,1}) && ischar(key) && strcmp(options{i,1},key)) || (isnumeric(options{i,1}) && isnumeric(key) && (options{i,1}==key)))
        my_flag = 1;
    end
end



end

