import time,sys

def pause_with_countdown(interval):

    for i in range(1,interval+1):
        if(not ((i % 2)==0)):
            sys.stdout.write(str(i)+'%d-',i);
            sys.stdout.flush()
        time.sleep(1);
    
    print('done!\n');
