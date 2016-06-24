function [ kv_map ] = kvs( key, val, kv_map, varargin )

[ kv_map ] = kv_set( key, val, kv_map, varargin{:} );