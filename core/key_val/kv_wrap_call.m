function out_dict = kv_wrap_call(f_handle, keys, dict)

%there must be a better way of doing this...

if(~exist('dict','var'));dict = {};end;

n_outputs = length(keys);

if(n_outputs==1)
    o1=f_handle();
    out_dict = kv_multiset(dict,keys{1},o1);
elseif(n_outputs==2)
    [o1,o2]=f_handle();
    out_dict = kv_multiset(dict,keys{1},o1,keys{2},o2);
elseif(n_outputs==3)
    [o1,o2,o3]=f_handle();
    out_dict = kv_multiset(dict,keys{1},o1,keys{2},o2, keys{3},o3);
elseif(n_outputs==4)
    [o1,o2,o3,o4]=f_handle();
    out_dict = kv_multiset(dict,keys{1},o1,keys{2},o2, keys{3},o3,keys{4},o4);
elseif(n_outputs==5)
    [o1,o2,o3,o4,o5]=f_handle();
    out_dict = kv_multiset(dict,keys{1},o1,keys{2},o2, keys{3},o3,keys{4},o4,keys{5},o5);
elseif(n_outputs==6)
    [o1,o2,o3,o4,o5,o6]=f_handle();
    out_dict = kv_multiset(dict,keys{1},o1,keys{2},o2, keys{3},o3,keys{4},o4,keys{5},o5,keys{6},o6);
elseif(n_outputs==7)
    [o1,o2,o3,o4,o5,o6,o7]=f_handle();
    out_dict = kv_multiset(dict,keys{1},o1,keys{2},o2, keys{3},o3,keys{4},o4,keys{5},o5,keys{6},o6,keys{7},o7);
end

