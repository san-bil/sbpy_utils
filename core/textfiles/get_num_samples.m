function [ num_samples ] = get_num_samples( file_path )


% in: file path, where contained newline separated samples

% out: number of event observations in file.

% desc: Given a file where columns represent variables and rows  
% represents samples, counts the number of samples in the file

% tags: #samples #rows #dataset

fid = fopen(file_path);
num_samples = 0;

tline = ' ';

while ischar(tline)
    
    
    tline = fgets(fid);
    
    if(size(tline,2)>1)
        num_samples = num_samples+1;
    else
        
    end
      
end

fclose(fid);

end

