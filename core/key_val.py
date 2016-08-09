import string,csv,copy,collections
from .command_line import touch
from collections import OrderedDict

def dict_filter(key_list, kvm):
    return dict((k, kvm[k]) for k in key_list if k in kvm)

def kv_filter(key_list, kvm):
    return dict((k, kvm[k]) for k in key_list if k in kvm)
    

def kv_to_file(kvm,kvfile):
    w = csv.writer(open(kvfile, "w"))
    for key, val in kvm.items():
        w.writerow([key, val])

def kv_read(kvfile):
    kvm = {}
    for key, val in csv.reader(open(kvfile)):
        kvm[key] = val
    return kvm


def kv_rm(key,kvm):
    out = copy.deepcopy(kvm)
    deleted=out[key]
    del out[key]
    return (out,deleted)

def kv_set(key,val,kvm,force_copy=False):
    if force_copy:
        return_dict=copy.deepcopy(kvm)
    else:
        return_dict=kvm
    return_dict[key]=val
    return return_dict


def kv_print(kvm,depth=0):
    for f in kvm:
        if(isinstance(kvm[f],dict)):
            print(str(f)+" : ")
            kv_print(kvm[f],depth+1)
        else:
            print(('  ' * depth)+str(f)+" : "+str(kvm[f]))

def kv_write_to_str_test():
    x=OrderedDict()
    x['a']='1'
    x['b']='2'
    x['c']=OrderedDict({'a':1,'b':2,c:{'x':23,'y':24,'z':25}})
    x['d']=OrderedDict({'l':10,'m':12,c:{'p':20,'q':21,'r':22}})
    new_str=kv_write_to_str(x)

def kv_write_to_str(kvm,depth=0,acc=''):
    for f in kvm:
        if(isinstance(kvm[f],dict)):
            acc += (str(f)+" : \n")
            acc += kv_write_to_str(kvm[f],depth+1)
        else:
            acc+=(('  ' * depth)+str(f)+" : "+str(kvm[f])+'\n')
    return acc

def kv_get(key, kvm, default=None):
    if key in kvm:
        return kvm[key]
    else:
        return default

def kvg(*args):
    return kv_get(*args)

def kv_get_vals(kvm):
    out=[]
    for f in kvm:
        out.append(kvm[f])
    return out

def kv_apply(kvm,func):
    if(isinstance(kvm, OrderedDict)):
        tmp = OrderedDict()
        for key in kvm:
            tmp[key]=func(kvm[key])
        return tmp
    else:
        return {k: func(kvm[k]) for k in kvm}

def kv_set_recurse(keylist,val,kvm):
    curr=kvm
    for i in range(0,len(keylist)):
        if keylist[i] in curr:
            curr=curr[keylist[i]]
        else:	
            if(not i==len(keylist)-1):
                curr[keylist[i]]={}
            else:
                curr[keylist[i]]=val
            curr=curr[keylist[i]]
    return kvm

def kv_get_recurse(keylist,kvm,default=None):
    curr=kvm
    for key in keylist:
        if key in curr:
            curr=curr[key]
        else:
            return default
        
    return curr

def test_kv_recursion():
    kvm={}
    kv_set_recurse(['a','b'],2,kvm)
    kv_set_recurse(['a','c'],4,kvm)
    kv_set_recurse(['a','f','g'],5,kvm)
    print( kv_get_recurse(['a','f','g'],kvm))
    
    
def kv_join(kv_1, kv_2):
    kv_3 = kv_1.copy()
    kv_3.update(kv_2)
    return kv_3
    
def test_kv_join():
    a={'a':1,'b':2}
    b={'c':3,'d':4}
    print(kv_join(a,b))

#test_kv_recursion()

def kv_append_val(key, val, kvm):
    default=[]
    curr=kvg(key,kvm,default)
    curr.append(val)
    kvm[key]=curr
    return kvm

def kv_append_numval(key, val, kvm):
    return kv_append_val(key, val, kvm)

    
def kv_update(updater_dict, parent_dict, force_copy=False):

    if force_copy:
        return_dict=copy.deepcopy(parent_dict)
    else:
        return_dict=parent_dict
        
    for key in updater_dict:
        if((key in parent_dict)):
            print('Overwriting dict value for '+str(key));
        return_dict[key] = updater_dict[key]
    return return_dict

def get_mutable_opts(key,opts_kv_file,default):

    try:
        touch(opts_kv_file)
        kvm = kv_read( opts_kv_file )
        out = kv_get(key,kvm,default)
    except Exception as err:
        print(err)
        out=default
    return out

def kv_wrap_call(fhandle,keys,kvm={}):
        
    fhandle_res=fhandle()
    if(isinstance(fhandle_res, tuple)):
        return {keys[i]:fhandle_res[i] for i in range(0,len(keys))}
    else:
        if(len(keys)==1):
            return {keys[0]:fhandle_res}
        else:
            raise TypeError()
    
    
def test_kv_wrap_call():
    fhandle=lambda:(1,2,3)
    kv_print(kv_wrap_call(fhandle, ['a','b','c']))
    print('---')
    kv_print(kv_wrap_call(fhandle, ['a','b']))
    print('---')
    kv_print(kv_wrap_call(fhandle, ['a']))
    print('---')
    kv_print(kv_wrap_call(fhandle, []))
    print('---')
    


def kv_print2(kvm,depth=0):
    try:
        import numpy as np
        
        for f in kvm:
            if(isinstance(kvm[f],dict)):
                print(str(f)+" : ")
                kv_print(kvm[f],depth+1)
            else:
                if(isinstance(kvm[f], np.ndarray)):
                    print(('  ' * depth)+str(f)+" : "+str('NDARRAY'))
                else:
                    print(('  ' * depth)+str(f)+" : "+str(kvm[f]))
    except Exception as err:
        print(err)

def kv_filter_long_keys(kvm,key_max_length=31, depth=1):   
    kvm_copy=copy.deepcopy(kvm)
    for f in kvm:
        if(isinstance(f,str) and len(f)>key_max_length):
            print('\nWARNING: removing %s from dictionary at depth %d\n' % (f,depth))
            kvm_copy=kv_rm(f,kvm_copy)[0]
        elif(isinstance(kvm[f],dict)):
            kvm_copy[f] = kv_filter_long_keys(kvm_copy[f], key_max_length, depth+1)

    return kvm_copy


def kv_print_keys_recurse(kvm,depth=0):
    try:        
        
        for f in kvm:
            print(('  ' * depth)+str(f)+" : "+str(len(str(f))))
            
            if(isinstance(kvm[f],dict)):
                kv_print_keys_recurse(kvm[f],depth+1)
    except Exception as err:
        print(err)
        
        
def kv_cwn(*args):
    res=OrderedDict()
    for i in range(0,len(args),2):
        res[args[i]]=args[i+1]
    return res

def test_kv_cwn():
    import pprint
    pprint.pprint(kv_cwn('a',1,'b',2,'c',3))
    
def kv_flip_keyvals(kvm):
    return dict((v,k) for k,v in kvm.iteritems())
