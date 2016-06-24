

def sanitize_string( x, sanitizer='_'):    
    y=x.lower();
    
    y.replace('    ',sanitizer);
    y.replace('   ',sanitizer);
    y.replace('  ',sanitizer);
    y.replace(' ',sanitizer);
    return y

def concat_string_list(arr,delim='_'):
    return delim.join(arr)

def filter_empty_strings(str_list):
    return filter(None, str_list)

def multifilter_string_list(list_arg,filters,exclusive=False):
    if(exclusive):
        return [line for line in list_arg if sum(map(lambda x: x in line, filters))==0]
    else:
        return [line for line in list_arg if sum(map(lambda x: x in line, filters))>0]
    

#from sbmat_core.command_line import my_system
#print(multifilter_string_list(my_system('find $HOME -maxdepth 1').split('\n'),['prezto'],False))