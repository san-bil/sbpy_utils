import os

def change_file_ext(arg,new_ext):
    return os.path.splitext(arg)[0]+'.'+new_ext

print(change_file_ext('/home/sanjay.png', 'jpg'))