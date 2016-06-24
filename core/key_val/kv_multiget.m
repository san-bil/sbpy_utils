function out = kv_multiget(map,keys)


filtered = kv_filter(map,keys,'include');


out = filtered(:,2);