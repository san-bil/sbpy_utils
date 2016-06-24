function outs = get_random_word(n_words)

if(~exist('n_words','var'));n_words=1;end

bash_script_path = prepend_path(dirname(mfilename('fullpath')),'random_word.sh');
cmd = build_string_args({'bash',bash_script_path, my_num_to_str(n_words)});

[~, out] = system(cmd);
out = strrep(out,'''','');

outs = filter_empty_strings(strsplit(out,'\n'));