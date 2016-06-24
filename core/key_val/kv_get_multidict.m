function [ val ] = kv_get_multidict( key,default,varargin )

val=default;
for i=1:length(varargin)
    
    val=kv_get(key,varargin{i},val);
    
end