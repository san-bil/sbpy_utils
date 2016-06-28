import operator as op
from collections import OrderedDict
import copy
import sbpy_utils.core.key_val as kv
from sbpy_utils.core.key_val import kv_get,kv_wrap_call,kv_rm,kv_join

def apply_func_pipeline_masked(input_arg, named_func_pipeline, mask=[], invert_mask=True):

    if not mask:
        mask=[True]*len(named_func_pipeline)

    tmp2 = input_arg    
    for pipeline_stage_name in named_func_pipeline:
        if(op.xor(invert_mask, (pipeline_stage_name in mask))):
            func_handle = named_func_pipeline[pipeline_stage_name]
            tmp3=func_handle(tmp2)
            if(isinstance(tmp3, tuple)):
                tmp2=tmp3[0]
            else:
                tmp2=tmp3
                
    return tmp2



def add_to_masking_func_pipeline(name, func, idx, pipeline):

    new_pipeline = OrderedDict({})
    ctr=0
    for key in pipeline:
        if(ctr==idx):
            new_pipeline[name]=func
    new_pipeline[key]=pipeline[key]
    ctr += 1


def apply_func_pipeline_masked_wrapped(input_arg, named_func_pipeline, mask, invert_mask):
    
    tmp = {}
    tmp['operand']=input_arg

    for pipeline_stage_name in named_func_pipeline:
        if op.xor(invert_mask, pipeline_stage_name in mask):

            func_handle = named_func_pipeline[pipeline_stage_name]['func_handle'];
            output_keys = named_func_pipeline[pipeline_stage_name]['output_keys']
            operand = kv_get('operand', tmp)
            func_handle_closed = lambda:func_handle(operand)
            new_tmp = kv_wrap_call(func_handle_closed, output_keys);
            [new_tmp_operand_free,new_operand] = kv_rm('operand',new_tmp);
            tmp = kv_join(tmp, new_tmp_operand_free);
            tmp['operand']=new_operand
        
        
    
    output=tmp['operand']  
    other_outputs,_= kv.kv_rm('operand',tmp);
    return (output, other_outputs)