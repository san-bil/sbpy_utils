function out = islocalhost(host)

out = strcmp(host,'localhost') || ~is_remote_host(host);