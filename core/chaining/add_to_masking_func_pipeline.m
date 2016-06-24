function new_pipeline = add_to_masking_func_pipeline(name, func, idx, pipeline)

new_pipeline = [pipeline(1:idx-1,:);{name,func};pipeline(1:idx+1,:)];
