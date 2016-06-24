function out = path_join_w_ext(varargin)

out = concat_cell_string_array(varargin(1:end-1),filesep,1);

out = strrep(out,'//','/');

out = [out '.' varargin{end}];