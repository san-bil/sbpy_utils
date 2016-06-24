function out = time_map_to_secs(map)

hour = kv_get('hour',map);
minute = kv_get('minute',map);
second = kv_get('second',map);
millis = kv_get('millis',map);

out = (3600*hour)+(60*minute)+second+(millis/1000);