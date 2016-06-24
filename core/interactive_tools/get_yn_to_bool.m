function res = get_yn_to_bool()

res= @(tmp)kv_get(tmp,kv_cwn('y',1,'n',0));