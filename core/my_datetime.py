import datetime

def get_simple_date():
    return str(datetime.datetime.now()).replace(':','_').replace(' ','_')

