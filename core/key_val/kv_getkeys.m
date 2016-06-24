function [ keys ] = kv_getkeys( kv_map )


% in: a 2-column cell array representing a dictionary (first column==string keys, second column==values)
%
% out: all the string-keys in the dictionary
%
% desc: as above.
%
% tags: #map #dictionary #associativearray #associative #keyvalue

keys = kv_map(:,1);

end

