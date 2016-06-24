function [ res ] = kv_get_recursive(keylist, kv_map, unsafe, varargin )

if(~exist('unsafe','var'))
    unsafe=0;
end

tmp=kv_map;
for i=1:length(keylist)

    
    tmp = kv_get(keylist{i},tmp,varargin{:});
    if((~iscell(tmp) && size(tmp,1)<2) && unsafe)
        break;
    end
    
end
res=tmp;

end

