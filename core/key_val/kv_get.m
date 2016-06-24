function [ val,idx ] = kv_get( key,kv_map,default_val,col_idx )

% in: a string key, a 2-column cell array representing a dictionary (first column==string keys, second column==values), 
% (optional) a default value to be returned if there is no matching key
%
% out: the associated value, or a default value is there is no matching key
%
% desc: as above.
%
% tags: #map #dictionary #associativearray #associative #keyvalue

if(iscell(key))
    error('kv_get: Key must be a string or double type.')
end

if(~exist('col_idx','var'))
    col_idx=2;
end

my_flag = 0;
val=[];
for i=1:size(kv_map,1)
    if((ischar(kv_map{i,1}) && ischar(key) && strcmp(kv_map{i,1},key)) || (isnumeric(kv_map{i,1}) && isnumeric(key) && all(kv_map{i,1}==key)) || (islogical(kv_map{i,1}) && islogical(key) && all(kv_map{i,1}==key)))
        val = kv_map{i,col_idx};
        idx = i;
        my_flag = 1;
    end
end

if(my_flag==0)
    if(exist('default_val','var'))
        val=default_val;
        if(ischar(key))
            print_log_message(2,1,'Using default val for %s\n', key);
        end
        idx=-1;
    else
        error('kv_get() - Key not found!');
    end
end

end

