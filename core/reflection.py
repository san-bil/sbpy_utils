import inspect

def get_caller():
    mycaller=inspect.getouterframes(inspect.currentframe(), 3)[1][3]
    return mycaller

def get_func_name():
    mycaller=inspect.getouterframes(inspect.currentframe(), 2)[1][3]
    return mycaller

