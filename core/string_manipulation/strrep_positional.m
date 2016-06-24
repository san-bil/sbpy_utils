function out = strrep_positional(in,replacee,replacer,idxs)

out = in;
match_locations = (regexp(in,replacee));
if(idxs==-1)
  out(match_locations(end)) = replacer;

else
    out(match_locations(idxs)) = replacer;
end