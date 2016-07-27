import string
import csv
import copy 
#import scipy.io
import cloudpickle
import file_system

def my_readlines(file_path):
    fo = open(file_path, "r")
    line = [line.replace('\n','') for line in fo.readlines()]
    fo.close()
    return line

def my_writelines(str_array,file_path):
    to_write='\n'.join([str(s) for s in str_array])
    easy_file_append_fast(to_write, file_path)

def my_save(kvm,file_path):
    cloudpickle.dump( kvm, open(file_path, "wb" ) )

def my_load(file_path):
    return cloudpickle.load( open(file_path, "rb" ) )

def savemat(*args, **kwargs):
    raise NotImplementedError()
    #scipy.io.savemat(*args, **kwargs)

def loadmat(*args, **kwargs):
    raise NotImplementedError()
    #return scipy.io.loadmat(*args, **kwargs)

def easy_file_append_num(arr,file_path):
    text= ''.join(map(lambda(tmp):('%f\n' % tmp),arr))
    easy_file_append_fast(text,file_path)
    
    
def easy_file_append_fast(to_write,file_path):
    fid = open(file_path, 'a+')
    fid.write(to_write)
    fid.close()
    