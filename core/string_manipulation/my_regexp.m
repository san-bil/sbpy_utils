function [out, matches] = my_regexp(in_str, matcher)

[r_start,r_end]=regexp(in_str,matcher);

if(~isempty(r_start) && ~isempty(r_end))
    out = mat2cell([r_start' r_end'],ones(length(r_start),1),2);

    matches = cellfun_uo0(@(tmp)in_str(tmp(1):tmp(2)), out);
else
    matches = {};
end