function kv_to_file(kv_map,kv_map_file_location,varargin)


% in: a 2-column cell array representing a dictionary (first column==string keys, second column==values), 
% the full path of the file to write to
%
% out: nada.
%
% desc: Writes dictionary/key-value map to a text file, with ability to align the equality signs for readability.
% Output file is like an .ini file, containing simple key value pairs.
%
% tags: #map #dictionary #associativearray #associative #keyvalue #file #ini

max_key_length = max(cellfun(@length,kv_map(:,1)));
kv_map_file_handle = fopen(kv_map_file_location,'w');

for i = 1:size(kv_map,1)

    option_key = kv_map{i,1};
    option_value = kv_map{i,2};

    key_length = length(option_key); 
    
    if(ismember('justified',varargin))
        key_length_diff = max_key_length-key_length;
    else
        key_length_diff=0;
    end
    if(sum(size(option_value)>1)>0 && iscell(option_value))
        %this means that if you don't have simple keyval pairs in the
        %options object, ignore those pairs with value of a more complex datatype.
    else
        if(ischar(option_value))
            option_string = [option_key,sprintf('%s = ',repmat(' ',1,key_length_diff)),option_value];
        elseif(isnumeric(option_value))
            option_string = [option_key,sprintf('%s = ',repmat(' ',1,key_length_diff)),num2str(force_fat_matrix(option_value))];
        end
        fprintf(kv_map_file_handle,'%s\n',option_string);
    end
end

fclose(kv_map_file_handle);


