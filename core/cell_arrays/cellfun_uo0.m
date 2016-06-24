function out = cellfun_uo0(f_handle,varargin)


out = force_skinny_matrix(cellfun(f_handle,varargin{:},'UniformOutput',0));