from collections import OrderedDict
import itertools
import numpy as np

def cartprod(*args):
    cartprod_res=[]
    for element in itertools.product(*args):
        cartprod_res.append(element)
    return cartprod_res
    

def generate_parameter_sets(parameter_ranges):

    ordered_param_ranges=OrderedDict()
    for k in parameter_ranges:
        ordered_param_ranges[k]=parameter_ranges[k]

    if(len(ordered_param_ranges)==0):
        parameter_sets=[];
    else:
        ranges = [ordered_param_ranges[r] for r in ordered_param_ranges]

    parameter_sets_raw = cartprod(*ranges);
    parameter_sets = []

    ordered_keys=ordered_param_ranges.keys()
    for param_set in parameter_sets_raw:
        
        parameter_instance = {key:param_set[i] for i,key in enumerate(ordered_keys)}
        parameter_sets.append(parameter_instance)
        
    return parameter_sets

def  gridsearch_optimizer_async(parameter_ranges,f_handle,synchronization_fhandle=(lambda :-1), results_fetcher_fhandle=(lambda :-1), create_param_instance_folders=0):

    dont_collect=results_fetcher_fhandle()==-1
        

    parameter_sets = generate_parameter_sets(parameter_ranges);

    for i in range(0,len(parameter_sets)):
    
        parameter_instance = parameter_sets[i]
    
        if(create_param_instance_folders):
            f_handle(parameter_instance, i);
        else:
            f_handle(parameter_instance);

        synchronization_fhandle();

    if(dont_collect):
        res_map={};
        fmin = np.inf
        xmin = np.inf
        f_acc_mat={}
    else:
    
        f_acc_mat = results_fetcher_fhandle();
        
        inverse_lookup=dict((v,k) for k,v in f_acc_mat.iteritems())
        
        fmin=np.min(f_acc_mat.values())
        xmin=inverse_lookup[fmin]
            
    return (xmin, fmin, f_acc_mat)




def gridsearch_optimizer_sync(parameter_ranges,f_handle,create_param_instance_folders):
    raise NotImplementedError()
    #if(~exist('create_param_instance_folders','var'));create_param_instance_folders=0;end;
    
    #parameter_sets = generate_parameter_sets(parameter_ranges);
    
    
    #res_map = {};
    
    #x_acc = cell(size(force_skinny_matrix(parameter_sets),1),1);
    #f_acc = zeros(size(force_skinny_matrix(parameter_sets),1),1);
    #for i = 1:size(parameter_sets,1)
    
        #parameter_instance = parameter_sets{i};
    
        #fprintf('Instantiating model:\n\n')
        #kv_print(kv_prefix_all_keys('       ',parameter_instance));
    
        #if(create_param_instance_folders)
            #[f_val]=f_handle(parameter_instance, i);
        #else
            #[f_val]=f_handle(parameter_instance);
        #end
    
    
        #res_map(i,1:2) = {i,kv_create(parameter_instance,f_val)};
        #x_acc{i} = parameter_instance;
        #if(isnumeric(f_val))
            #f_acc(i) = f_val;
        #else
            #try
                #f_acc(i) = kv_get('simple_fitness_val',f_val);
            #catch myerr
                #disp('WARNING: Setting f_acc(i) to Inf since the function handle to gridsearch_optimizer_sync() didn''t return a simple_fitness_val.')
                #f_acc(i) = Inf;
            #end
    
        #end
    #end
    
    #fmin=min(f_acc);
    #xmin=x_acc{argmin(f_acc)};
    return (xmin, fmin, res_map)
