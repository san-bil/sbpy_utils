function res = is_ssh_host_responding(stdout_lines)

res = ~any(cell2mat(cellfun_uo0(@(tmp)logical(length(regexp(tmp,'Connection timed out'))),stdout_lines)));

