function outs = get_random_word_puremat(n_words)

if(~exist('n_words','var'));n_words=1;end

folder=dirname(mfilename('fullpath'));

cmd = build_string_args({'shuf','-n',my_num2str(n_words),path_join(folder,'words.txt')});

[~, out] = system(cmd);
out=strrep(out,'''','');

outs = filter_empty_strings(strsplit(out,'\n'));

outs2 = cellfun_uo0(@(tmp)[upper(tmp(1)) tmp(2:end)], outs);
