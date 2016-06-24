function out = strrep_multi(in, varargin )

out=in;
for i = 1:2:length(varargin)
    
    replacee = varargin{i};
    replacer = varargin{i+1};
    out = strrep(out,replacee,replacer);
end
