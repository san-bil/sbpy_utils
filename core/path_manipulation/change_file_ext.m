function out = change_file_ext(file_path,target_ext)

dots = regexp(file_path,'\.');

if(isempty(dots))
    file_path = [file_path '.'];
    dots = length(file_path);
end

out = [file_path(1:dots(end)) target_ext];