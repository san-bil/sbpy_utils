function str=concat_cell_string_array(cell_string_array,delim,conservative)

if(isempty(cell_string_array))
    str='';
else
        
    if(~exist('delim','var'))
        delim=';';
    end

    if(~exist('conservative','var'))
        conservative=0;
    end

    if(conservative)

        for i = 1:length(cell_string_array)
            if(i>1)
                str = [str delim cell_string_array{i}];
            else
                str = cell_string_array{i};
            end
        end

    else
        str='';
        for i = 1:length(cell_string_array)
            str = [str delim cell_string_array{i}];
        end
    end
end