function map = kv_append_vals(map, varargin)

if(mod(length(varargin),2)~=0)
    error('non-matching number of keys and values')
end


for i = 1:floor(length(varargin)/2)
    idx=((i-1)*2)+1;
    var_name = varargin{idx};
    var_val = varargin{idx+1};
    map = kv_append_val(var_name,var_val,map);
end

