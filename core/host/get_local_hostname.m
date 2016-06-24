function [ hostname ] = get_local_hostname( )

% in: nada
%
% out: system hostname
%
% desc: returns system's hostname
%
% tags: hostname

[~,raw_hostname]=system('hostname');
hostname = strtrim(raw_hostname);
end

