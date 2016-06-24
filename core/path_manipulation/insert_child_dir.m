function out = insert_child_dir(to_insert, in)

[curr_parent, curr_child] = get_parent_dir(in);

out = [curr_parent filesep to_insert filesep curr_child ];