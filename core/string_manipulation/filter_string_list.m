function out = filter_string_list(list,regex,exclusive)

if(~exist('exclusive','var'))
    exclusive=0;
end

if(exclusive)
    mask_mod = @(tmp)~tmp;
else
    mask_mod = @(tmp)tmp;
end

filter = @(tmp) ~isempty(regexp(tmp, regex, 'once'));
mask = cellfun(filter, list, 'UniformOutput',0);
out = list(mask_mod(cell2mat(mask)));