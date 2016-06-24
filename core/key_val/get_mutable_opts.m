function out = get_mutable_opts(key,opts_kv_file,default)

try
    touch(opts_kv_file);
    map = kv_read( opts_kv_file );
    out = kv_get(key,map,default);
catch err
    disp(err);
    out=default;
end
