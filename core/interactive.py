from collections import OrderedDict



import string

def user_prompt_loop(initial_prompt, input_filters_w_failure_responses):


    while True:
    
        user_input = raw_input(initial_prompt);
    
        flag=True
        for myfilter,response in input_filters_w_failure_responses:
            filter_res=myfilter(user_input)
            if not filter_res:
                print(response)
            flag = flag and filter_res
            
        
        if(flag):
            return user_input;
    
def get_yn_to_bool():
    fhandle = lambda x: {'y':True, 'n':False, '1':True, '0':False}[x]
    return fhandle

def get_interactive_opt(choices, prompt="INTERACTIVE - ", fhandle=(lambda x:x)):
    choices_str=string.join(choices,', ')
    choice=user_prompt_loop(prompt+' ('+choices_str+') : ' , [(lambda x: ((x in choices) or len(choices)==0),'Please enter one of: '+choices_str)]);
    choice=fhandle(choice);
    return choice

    