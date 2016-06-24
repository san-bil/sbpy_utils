function out=write_cell_of_strings_to_file(filepath,string_arr)

if(nargin==0)
    fprintf('\n\tUsage: write_cell_of_strings_to_file(filepath,string_arr)\n\n');
    return
end

touch(filepath);
fid=fopen(filepath,'a');

csvFun = @(str)sprintf('%s\n,',str);

xchar = cellfun(csvFun, string_arr, 'UniformOutput', false);

xchar = strcat(xchar{:});

xchar = strcat(xchar(1:end-1),'\n');
fprintf(fid,strrep(xchar,',',''));
fclose(fid);
out=1;