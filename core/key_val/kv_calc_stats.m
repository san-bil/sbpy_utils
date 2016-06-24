function stats_map =kv_calc_stats(map)

keys=kv_getkeys(map);

stats_map = {};
for i =1:length(keys)

    key = keys{i};
    val = kv_get(key,map);
    
    if(iscell(val))
        val = cell2mat(val);
    end
    
    val_mean = mean(val);
    val_std = std(val);
    
    stats_map = kv_set([key,'_mean'],val_mean,stats_map);
    stats_map = kv_set([key,'_std'],val_std,stats_map);
    
end