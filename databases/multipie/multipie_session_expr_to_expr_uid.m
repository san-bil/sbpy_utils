function expr_uid=multipie_session_expr_to_expr_uid(session,expr)

map={};

% neutral=1;
% smile=2;
% surprise=3;
% squint=4;
% disgust=5;
% scream=6;

neutral=0;
smile=1;
surprise=2;
squint=3;
disgust=4;
scream=5;

map = kv_set_recurse({1,1},neutral,map);
map = kv_set_recurse({1,2},smile,map);

map = kv_set_recurse({2,1},neutral,map);
map = kv_set_recurse({2,2},surprise,map);
map = kv_set_recurse({2,3},squint,map);

map = kv_set_recurse({3,1},neutral,map);
map = kv_set_recurse({3,2},smile,map);
map = kv_set_recurse({3,3},scream,map);


map = kv_set_recurse({4,1},neutral,map);
map = kv_set_recurse({4,2},neutral,map);
map = kv_set_recurse({4,3},scream,map);

expr_uid=arrayfun(@(t1,t2)kv_get_recursive({t1,t2}, map), session, expr);