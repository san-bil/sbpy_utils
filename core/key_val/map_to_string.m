function str_acc = map_to_string(map)

mask = cellfun(@isnumeric,map(:,2)) | cellfun(@ischar,map(:,2));
assert(sum(mask)==length(mask));

str_acc = '';

for i = 1:length(map)
   str_acc = [str_acc '_' map{i,1} '_' num2str(map{i,2})]; 
end