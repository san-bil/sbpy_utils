import numpy as np
import time
from PIL import Image

def imread_safe(img_path,pause_time=2,colorspace='RGB'):

    ctr=0

    for i in range(0,10):
        try:
            img = np.asarray( Image.open(img_path))
            return img
        except Exception as err:
            print(str(err))
            ctr += 1;
            if(ctr==30):
                raise(myerr);
            else:
                print('imread_safe(): cant read image '+img_path+', trying again in '+str(pause_time)+' secs. \n');
                time.sleep(pause_time)
    