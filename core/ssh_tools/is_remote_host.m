function out = is_remote_host(in)

out = ~strcmp(in,get_local_hostname());