function out = get_random_name()

bash_script_path = prepend_path(dirname(mfilename('fullpath')),'random_name.sh');
cmd = build_string_args({'bash',bash_script_path});

[~, out] = system(cmd);
