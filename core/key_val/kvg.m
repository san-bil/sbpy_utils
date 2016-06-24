function [ val,idx ] = kvg( key,kv_map,varargin )

[ val,idx ] = kv_get( key,kv_map,varargin{:});