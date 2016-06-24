function varargout = kv_multiget2(map,keys)


filtered = kv_filter(map,keys,'include');


varargout = filtered(:,2);

