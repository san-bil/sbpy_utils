function log_level = get_function_verbosity(opts)

cf = callerfunc();

log_level = kv_get([cf '_log_level'], opts,0);