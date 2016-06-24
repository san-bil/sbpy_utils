def my_num2str(x):
     return my_num_to_str(x);

def my_num_to_str(x):
     return str(x)

def  my_str_to_num(x):
     return float(x)

def vect2str( vect ):
     return '[ '+(''.join(map(lambda(x):(str(x)+', '),(list(vect)))))[:-2]+']'

import sys
for f in sys.path:
     print(f)

import numpy as np
print(vect2str(np.arange(1,5)))

