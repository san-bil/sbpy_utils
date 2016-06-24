function lines = parse_stdout(stdout)

lines = filter_empty_strings(strsplit(stdout,'\n'))';
