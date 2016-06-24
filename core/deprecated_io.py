import string
import csv
import copy 

def my_readlines(file_path):
    fo = open(file_path, "r")

    line = [line.replace('\n','') for line in fo.readlines()]

    fo.close()
    return line


