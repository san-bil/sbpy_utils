function out = path_join(varargin)

out = concat_cell_string_array(varargin,filesep,1);

out = strrep(out,'//','/');