function out = get_random_uname()

if(~exist('n_words','var'));n_words=3;end

bag = get_random_word_puremat(n_words);

out = concat_cell_string_array(cellfun_uo0(@(tmp)regexprep(tmp,'(\<[a-z])','${upper($1)}'), bag),'');