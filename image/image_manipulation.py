import numpy as np
from my_io import imread_safe
from skimage import color
#from skimage.transform import resize
import cv2 
from PIL import Image
import matplotlib.pyplot as plt

def concat_images_horiz(imga, imgb):
    """
    Combines two color image ndarrays side-by-side.
    """
    ha,wa = imga.shape[:2]
    hb,wb = imgb.shape[:2]
    max_height = np.max([ha, hb])
    total_width = wa+wb
    new_img = np.zeros(shape=(max_height, total_width, 3), dtype=np.uint8)
    new_img[:ha,:wa]=imga
    new_img[:hb,wa:wa+wb]=imgb
    return new_img

def concat_images_vert(imga, imgb):
    """
    Combines two color image ndarrays top-to-bottom.
    """
    ha,wa = imga.shape[:2]
    hb,wb = imgb.shape[:2]
    max_width = np.max([wa, wb])
    total_height = ha+hb
    new_img = np.zeros(shape=(total_height, max_width, 3), dtype=np.uint8)
    new_img[:ha,:wa]=imga
    #new_img[:hb,wa:wa+wb]=imgb
    new_img[ha:ha+hb,:wb]=imgb
    return new_img

def concat_n_images(images,direction='H'):
    """
    Combines N color images from a list of image paths.
    """
    if(len(images)==1):
        output=images[0]
    elif isinstance(images, np.ndarray):
        output=images
    else:    
        concatenator={'H':concat_images_horiz,'V':concat_images_vert}[direction]
        output = None
        for i, img in enumerate(images):
            
            if(len(img.shape)==2):
                img=np.expand_dims(img,2)
            
            if i==0:
                output = img[:,:,:3]
            else:
                output = concatenator(output,(img)[:,:,:3])
    return output


def imresize(img,new_size):
    if not isinstance(new_size,float) and len(new_size)==1:
        new_size=np.ceil(new_size[0]*img.shape)
    elif isinstance(new_size,float):
        new_size=np.ceil(map(lambda x:float(x)*new_size,img.shape))
    if(len(img.shape)>2):
        new_size[2:]=img.shape[2:]
    new_size=new_size.astype(int)
    res = cv2.resize(img, (new_size[1],new_size[0]))
    return res
    

def histeq(im,nbr_bins=256):

    #get image histogram
    imhist,bins = np.histogram(im.flatten(),nbr_bins,normed=True)
    cdf = imhist.cumsum() #cumulative distribution function
    cdf = 255 * cdf / cdf[-1] #normalize

    #use linear interpolation of cdf to find new pixel values
    im2 = interp(im.flatten(),bins[:-1],cdf)

    return im2.reshape(im.shape), cdf

def histmatch2(imsrc, imtint, nbr_bins=255):
    
    if len(imsrc.shape) < 3:
        imsrc = imsrc[:,:,np.newaxis]
        imtint = imtint[:,:,np.newaxis]
    
    imres = imsrc.copy()
    for d in range(0,imsrc.shape[2]):
        imhist,bins = np.histogram(imsrc[:,:,d].flatten(),nbr_bins,normed=True)
        tinthist,bins = np.histogram(imtint[:,:,d].flatten(),nbr_bins,normed=True)
    
        cdfsrc = imhist.cumsum() #cumulative distribution function
        cdfsrc = (255 * cdfsrc / cdfsrc[-1]).astype(np.uint8) #normalize
    
        cdftint = tinthist.cumsum() #cumulative distribution function
        cdftint = (255 * cdftint / cdftint[-1]).astype(np.uint8) #normalize
    
    
        im2 = np.interp(imsrc[:,:,d].flatten(),bins[:-1],cdfsrc)
    
    
    
        im3 = np.interp(im2,cdftint, bins[:-1])
    
        imres[:,:,d] = im3.reshape((imsrc.shape[0],imsrc.shape[1] ))    
    return imres

def histmatch(imsrc, histograms, nbr_bins=255):
    
    if len(imsrc.shape) < 3:
        imsrc = imsrc[:,:,np.newaxis]
    
    imres = imsrc.copy()
    for d in range(0,imsrc.shape[2]):
        imhist,bins = np.histogram(imsrc[:,:,d].flatten(),nbr_bins,normed=True)
        tinthist = histograms[d]
    
        cdfsrc = imhist.cumsum() #cumulative distribution function
        cdfsrc = (255 * cdfsrc / cdfsrc[-1]).astype(np.uint8) #normalize
    
        cdftint = tinthist.cumsum() #cumulative distribution function
        cdftint = (255 * cdftint / cdftint[-1]).astype(np.uint8) #normalize
    
    
        im2 = np.interp(imsrc[:,:,d].flatten(),bins[:-1],cdfsrc)
    
    
    
        im3 = np.interp(im2,cdftint, bins[:-1])
    
        imres[:,:,d] = im3.reshape((imsrc.shape[0],imsrc.shape[1] ))    
    return imres


def test():
    img = imresize(np.asarray(  ( Image.open('/Users/sanjay/Pictures/wallpaper/IMG_0437_2.JPG').convert('L') )),0.5)
    img2 = imresize(np.asarray(  ( Image.open('/Users/sanjay/Pictures/wallpaper/IMG_2522.JPG').convert('L') )),0.5)
    nbins=255
    empbins=90
    
    intensity_hgram = np.concatenate((np.zeros((empbins/2)), np.ones((nbins-empbins))*((185*250)/(nbins-empbins)), np.zeros((empbins/2))), 0)
    
    img3=histmatch(img2,[intensity_hgram])
    imgplot = plt.imshow(concat_n_images([img,img2,img3],'V'))
    #plt.imshow(imgwut)
    plt.show()

