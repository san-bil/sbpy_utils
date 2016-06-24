function [output, other_outputs]=apply_func_pipeline_masked_wrapped(input, named_func_pipeline, mask, invert_mask) 

tmp = kv_create_w_names('operand',input);

keys = kv_getkeys(named_func_pipeline);

for i = 1:length(keys)
    pipeline_stage_name = keys{i};

    if(xor(invert_mask, ismember(pipeline_stage_name,mask)))
        
        func_handle = kv_get_recursive({pipeline_stage_name,'func_handle'}, named_func_pipeline);
        output_keys = kv_get_recursive({pipeline_stage_name,'output_keys'}, named_func_pipeline);
        operand = kv_get('operand', tmp);
        func_handle_closed = @()func_handle(operand);
        new_tmp = kv_wrap_call(func_handle_closed, output_keys);
        [new_tmp_operand_free,new_operand] = kv_rm('operand',new_tmp);
        tmp = kv_join(tmp, new_tmp_operand_free);
        tmp = kv_set('operand', new_operand, tmp);
        
        
    end
end

[other_outputs, output] = kv_rm('operand',tmp);