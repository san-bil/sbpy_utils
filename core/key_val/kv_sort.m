function [ map ] = kv_sort(map)


keys = kv_getkeys(map);
vals = kv_get_vals(map);

[~,order]=sort(keys);

map = [keys(order) vals(order)];