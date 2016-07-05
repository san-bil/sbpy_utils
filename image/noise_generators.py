import numpy as np
from numpy import vectorize
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import time
import operator as op
from scipy.stats import threshold
import copy

def add_gaussian_noise_to_image(img,variance):
    
    tmp=threshold(img+np.random.normal(0,variance+0.00000000000000000000001,img.shape),0)
    return (tmp,copy.deepcopy(tmp))


def add_sparse_noise_to_image(img, probability, noise_generator=(lambda s: np.random.uniform(0,1,(s,1)))):

    img_area = (img.shape[0]*img.shape[1])
    bernoulli_mask =  np.random.uniform(0,1,(img.shape[0],img.shape[1]))>probability
    
    noise = noise_generator(np.sum(bernoulli_mask));
    noisy_img = np.zeros(img.shape)
    
    orig_shape=img.shape

    if(len(img.shape)<3):
        layer = noisy_img.flatten()
        layer[bernoulli_mask.flatten()]=noise
        noisy_img=layer
    else:
        for i in range(0,(img.shape[2])):
            layer = img[:,:,i].flatten()
            layer[bernoulli_mask.flatten()]=noise
            reshape_layer=layer.reshape(orig_shape[0:2])
            noisy_img[:,:,i] = reshape_layer
    

    return (noisy_img,bernoulli_mask)


def downsample_noise_support(init_noise_support,perc):
    noise_support=copy.deepcopy(init_noise_support)
    sampled_noise_idxs=np.random.choice(range(0,int(np.sum(noise_support))),int(np.round(np.sum(noise_support)*(1.0-perc))),replace=False)
    noise_idxs_to_wipe = sorted(sampled_noise_idxs);
    support = np.ravel_multi_index (np.nonzero(noise_support),noise_support.shape,order='C')
    to_wipe = support.ravel()[noise_idxs_to_wipe]
    to_wipe2 = np.unravel_index(to_wipe,noise_support.shape)
    noise_support[to_wipe2]=0
    return noise_support

def test_downsample_noise_support():
    x=np.round(np.random.uniform(0,1,(5,5)))
    xprime=downsample_noise_support(x, 0.5)
    
    print(x)
    print('\n\n\n\n')
    print(xprime)
