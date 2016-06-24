import os
from command_line import my_system, get_local_os
from string_manipulation import filter_empty_strings
import random

def get_random_word(n_words=1):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    shuf_cmd={'linux':'shuf','mac':'gshuf' }[get_local_os()]
    
    cmd = ' '.join([shuf_cmd,'-n',str(n_words),os.path.join(current_dir,'words.txt')]);
    
    cmd_res = my_system(cmd);
    cmd_res = cmd_res.replace("'","")

    outs = filter_empty_strings(cmd_res.split('\n'));

    outs2 = map(lambda tmp:tmp.title(), outs);

    return outs2


def get_random_uname(n_words=3):
    bag = get_random_word(n_words)
    return ''.join(bag);

def get_random_string(sLength):
    s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    s_list=list(s)
    randString = ''.join([random.choice(s_list) for i in range(0,sLength)])
    return randString

def get_random_hex_value(hex_length=5):
    hex_list=list('0123456789abcdef')
    return ''.join([random.choice(hex_list) for i in range(0,hex_length)]);

def run_all_tests():
    print(get_random_uname(5))
    print(get_random_string(10))
    print(get_random_hex_value(10))

#run_all_tests()