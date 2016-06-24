import os,sys
from os.path import dirname
sys.path.append(dirname(dirname(os.path.realpath(__file__))))
from core.key_val import kv_get,kv_update
import copy

def update_task_specific_model_opts(kvm,task_idx,force_copy=True):

    task_specific_model_opts_ctnr=kv_get('task_specific_model_opts',kvm,{})
    
    task_specific_model_opts=kv_get(task_idx,task_specific_model_opts_ctnr,{})
    
    out_dict = kv_update(task_specific_model_opts, kvm, force_copy)
    return out_dict

def test():
    print(update_task_specific_model_opts({'a':1,'b':2,'task_specific_model_opts':{2:{'a':3}}}, 1))
    print(update_task_specific_model_opts({'a':1,'b':2,'task_specific_model_opts':{2:{'a':3}}}, 2))
    

