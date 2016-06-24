function [pre,post] = strsplit_inc_delim(str,delim)

out = strsplit(str,delim);

pre=[out{1} delim];
post=out{2};