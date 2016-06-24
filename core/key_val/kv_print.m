function kv_print( input_args )


% in: a 2-column cell array representing a dictionary (first column==string keys, second column==values), 
%
% out: nada
%
% desc: prints the dictionary in human-readable form to stdout.
%
% tags: #map #dictionary #associativearray #associative #keyvalue

% prints contents of a keyval map, where the keyval map is a nx2 cell array.

for i = 1:size(input_args,1)
    
    if(isnumeric(input_args{i,2}))
       disp([input_args{i,1},' = ',vec_2_csv(force_fat_matrix(input_args{i,2}))])
    else
        disp([input_args{i,1},' = ',force_fat_matrix(input_args{i,2})])
    end
    
end

end

