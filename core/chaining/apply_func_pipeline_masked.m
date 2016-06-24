function [tmp2]=apply_func_pipeline_masked(input, named_func_pipeline, mask, invert_mask) 

tmp2 = input;

keys = kv_getkeys(named_func_pipeline);

for i = 1:length(keys)
    pipeline_stage_name = keys{i};

    if(xor(invert_mask, ismember(pipeline_stage_name,mask)))
        func_handle = kv_get(pipeline_stage_name, named_func_pipeline);
        tmp2=func_handle(tmp2);
    end
end

