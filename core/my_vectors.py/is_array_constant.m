function is_constant = is_array_constant(in)


tmp = all(in == in(1));

are_eq = nd_sum(tmp);

is_constant = are_eq==numel(tmp);

