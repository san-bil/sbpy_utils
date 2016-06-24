function out = homedir()


cmd = build_cmd({'echo $HOME'});
[~,stdout] = system(cmd);
out = parse_stdout(stdout);
out = out{1};
