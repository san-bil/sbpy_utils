import os, time, copy, sys,threading, random, math, itertools, numpy as np
from scipy.misc import imread
from Queue import Queue
from pathos.pools import ThreadPool
from collections import deque
from warnings import warn

import sbpy_utils.core.sets
import sbpy_utils.core.string_manipulation as stringman
from sbpy_utils.core.string_manipulation import concat_string_list,filter_empty_strings
from sbpy_utils.temporal.preprocessing import pad_sequences_tensor,depad_sequences_tensor,split_sequence_tensor,pad_sequence_list
from sbpy_utils.core.key_val import *
from sbpy_utils.core.command_line import my_system
import sbpy_utils.core.my_io
from sbpy_utils.core.chaining import *
from sbpy_utils.image.my_io import imread_safe
from sbpy_utils.core.list_tools import list_split
from random_words import RandomWords


get_copier=lambda tmp:{True:lambda tmp2:copy.deepcopy(tmp2),False:lambda tmp2:tmp2}[tmp]
rw=RandomWords()
get_random_name=lambda:'_'.join([rwstr.title() for rwstr in rw.random_words(count=3)])


class ImgCollection(object):
    def pixels(self):
        return [tmp.pixels() for tmp in self.data]
    
    def print_myname(self,leading_whitespace='',max_depth=10,curr_depth=0):
        print(leading_whitespace+self.myname)
        if(curr_depth<=max_depth):
            for f in self.data:
                f.print_myname(leading_whitespace=leading_whitespace+'  ',
                               max_depth=max_depth,
                               curr_depth=curr_depth+1)


class NestedImgCollection(object):
    def as_nested_list(self):
        return [tmp.as_nested_list() for tmp in self.data]    


class Offsettable():
    def offset(self,offset_length,docopy=True):
        if(docopy):
            new_self=self._nodata_copy()
            retobj=new_self
        else:
            retobj=self

        if offset_length < 0:
            retobj.data = retobj.data[np.abs(offset_length):]
            retobj.time_idxs=retobj.time_idxs[np.abs(offset_length):]
            retobj.length=retobj.length-offset_length
        elif offset_length > 0:
            retobj.data = retobj.data[:-np.abs(offset_length)]
            retobj.time_idxs=retobj.time_idxs[:-np.abs(offset_length)]
            retobj.length=retobj.length-np.abs(offset_length)
        elif offset_length==0:
            pass

        return retobj    


class OffsettableCollection():
    def offset(self,offset_length,docopy=True):
        if(docopy):
            new_self=self._nodata_copy()
            retobj=new_self
        else:
            retobj=self

        retobj.data = [tmp.offset(offset_length,docopy=False) for tmp in retobj.data]      
        return retobj


class Paddable():
    def pad_to_length(self,pad_length,docopy=True):

        if(docopy):
            new_self=self._nodata_copy()
            retobj=new_self
        else:
            retobj=self

        len_diff=pad_length-len(retobj.data)
        pad_idxs=range(len(retobj.data),pad_length)

        pad_img_list=[None]*len_diff
        for i,pad_idx in enumerate(pad_idxs):
            new_path=(self.video_path+':'+str(pad_idx)+'_pad')
            pad_img_list[i]=Img(np.zeros(self.shape()), path=new_path)

        retobj.data=retobj.data+pad_img_list
        return retobj

    def depad(self):
        self.data=self.data[:self.length]
    

class PaddableCollection():
    def pad_to_length(self,pad_length,docopy=True):

        if(docopy):
            new_self=self._nodata_copy()
            retobj=new_self
        else:
            retobj=self

        retobj.data = [tmp.pad_to_length(pad_length,docopy=False) for tmp in retobj.data]      
        return retobj
    
    def depad(self):
        self.data=[tmp.depad() for tmp in self.data]
    

def traverse_apply(obj, callback, tree_types=list,single_leaf=False):
    if isinstance(obj, tree_types):
        if single_leaf:
            idxs=0
        else:
            idxs=range(0,len(obj.data))

        for tmp in [obj.data[i] for i in idxs]:
            traverse_apply(tmp, callback, tree_types,single_leaf)
    else:
        callback(obj)
        tmp=1

class SingleViewImgTree():

    def print_other_data(self,key):
        assert(isinstance(self,ImgList) 
               or isinstance(self,Video) 
               or isinstance(self,VideoList))
        def tmpf(tmp):
            if key in tmp.other_data:
                print(tmp.other_data[key])
        traverse_apply(self, tmpf,tree_types=(ImgList,Video,VideoList))

    def assign_tensor_to_other_data(self, tensor, key, padded_length=None):

        assert(isinstance(self,ImgList) 
               or isinstance(self,Video) 
               or isinstance(self,VideoList))
        
        if not padded_length is None:
            if isinstance(self, VideoList):
                sequence_lengths=self.sequence_lengths()
                splitpoints=np.cumsum(np.asarray([padded_length]*len(sequence_lengths)))
                splitpoints=splitpoints[:-1]
                split_tl=[np.array_split(tmp,tmp.shape[0],axis=0)[:sequence_lengths[idx2]] for idx2,tmp in enumerate(np.split(tensor,splitpoints,axis=0))]
                split_tensor=list(itertools.chain.from_iterable(split_tl))
            if isinstance(self, Video):
                sequence_length=self.length
                split_tensor=np.array_split(tensor,tensor.shape[0],axis=0)[:sequence_length]

                
            
        split_tensor_q = deque(split_tensor)
        cb = lambda tmp:tmp.other_data.update({key:split_tensor_q.popleft()})

        traverse_apply(self, callback=cb,tree_types=(ImgList,Video,VideoList))
        if(len(split_tensor_q)>0):
            raise IndexError('Not all items in split_tensor_q consumed')
        tmp=1
        return 

    def fetch_from_other_data(self, key):

        assert(isinstance(self,ImgList) 
               or isinstance(self,Video) 
               or isinstance(self,VideoList))

        tensor_q = deque()
        cb = lambda tmp:tensor_q.append(tmp.other_data[key])

        traverse_apply(self, callback=cb,tree_types=(ImgList,Video,VideoList))
        return list(tensor_q)
    
    


class MultiViewImgTree():

    def multi_traverse_apply(callback,single_leaf=False):   
        for f in self.data:
            traverse_apply(f,callback,single_leaf)

    def print_other_data(self,key):
        for f in self.data:
            f.print_other_data(key)

    def assign_tensorlist_to_other_data(self, tensor_list, key,padded_length=None):
        for t,f in zip(tensor_list,self.data):
            f.assign_tensor_to_other_data(t,key,padded_length)

    def fetch_from_other_data(self, key):
        retval=[]
        for f in self.data:
            retval.append(f.fetch_from_other_data(key))
        return retval



def rand_string(N=5):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
    
class DummyClass(object):
    def __init__(self,**kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])


class Img():
    def __init__(self,data,path='',other_data=None):
        assert(isinstance(data,np.ndarray) or isinstance(data,DummyClass))
        self.data=data
        self.path=path
        if other_data is None:
            self.other_data = OrderedDict({})
        else:
            self.other_data=OrderedDict(other_data)        
        self.height=data.shape[0]
        self.width=data.shape[1]
        if data.ndim==3 :
            self.channels=data.shape[2]
        elif data.ndim==4:
            self.channels=data.shape[3]
        else:
            self.channels=1
        #self.other_data[rand_string()]=rand_string()
        
        self.myname=get_random_name()
 
            
    def _nodata_copy(self):
        new_img = Img(self.data,self.path,other_data=copy.deepcopy(self.other_data))
        return new_img
    
    def pixels(self):
        return self.data
    
    
    def print_myname(self,leading_whitespace='',max_depth=10,curr_depth=0):
        print(leading_whitespace+self.myname)
        if(curr_depth<=max_depth):
            print(leading_whitespace+self.myname)
    
    def as_tensor(self):
        if self.data.ndim==2 and self.data.shape[0]>1 and self.data.shape[1]>1:
            out=np.expand_dims(self.data,2)
        else:
            out=self.data
            
        if out.ndim == 3 and out.shape[0]>1 and out.shape[1]>1:
            out=np.expand_dims(out,0)
        elif out.ndim == 4:
            out = self.data
        else:
            out = self.data
            
        return out
    
    def from_tensor(self,tensor,docopy=True):
        if(tensor.ndim==4):
            n_tensor=np.squeeze(tensor,0)
        else:
            n_tensor=tensor
        
        if(docopy):
            new_self=Img(n_tensor,self.path,other_data=copy.deepcopy(self.other_data))
            ret_obj = new_self
        else:
            self.data=n_tensor
            ret_obj = self
        return ret_obj

    def shape(self):
        return self.data.shape
    
    def add_other_data(self,key,val):
        self.other_data[key]=val

class ImgGroup(ImgCollection):
    def __init__(self,imgs):
        assert(all([isinstance(x, Img) for x in imgs]))
        self.data=imgs
        self.myname=get_random_name()

    def _nodata_copy(self):
        return ImgGroup([tmp._nodata_copy() for tmp in self.data])
        
    def as_nested_list(self):
        return self.data

    def as_tensor(self,docopy=False):
        copier=get_copier(docopy)
        return [tmp.as_tensor() for tmp in copier(self.data)]

    def from_tensor_list(self,tensor_list,docopy=True):
        assert(isinstance(tensor_list, list))

        if(docopy):
            new_self=self._nodata_copy()
            ret_obj=new_self
        else:
            ret_obj=self
        
        tmp_imgs=[]
        for tmp_img,tmp_tensor in enumerate(zip(ret_obj.data,tensor_list)):
            tmp_img = tmp_img.from_tensor(tmp_tensor,docopy=False)
            tmp_imgs.append(tmg_imgs)
        self.data=tmp_imgs
            
        return ret_obj
            
    def shape(self):
        return [tmp.shape() for tmp in self.data]
    
    def num_views():
        return len(self.data)
    
    def add_other_data(self,key,vals):
        for img,val in zip(self.data,vals):
            img.add_other_data(key,vals)
    

class ImgList(ImgCollection,
              SingleViewImgTree):
    def __init__(self,imgs):
        assert(all([isinstance(x, Img) for x in imgs]))
        self.data=imgs
        self.myname=get_random_name()
    
    def __len__(self):
        return len(self.data)
    
    def _nodata_copy(self):
        return ImgList([tmp._nodata_copy() for tmp in self.data])
    
    def as_nested_list(self):
        return self.data
    
    def as_flat_list(self):
        return self.data
    
    def as_tensor(self):
        return np.concatenate(tuple([tmp.as_tensor() for tmp in self.data]),  0)
                
    def from_tensor_list(self,tensor_list,docopy=True):
        assert(isinstance(tensor_list, list))

        if(docopy):
            new_self=self._nodata_copy()
            ret_obj=new_self
        else:
            ret_obj=self
        
        tmp_imgs=[]
        for tmp_img,tmp_tensor in zip(ret_obj.data,tensor_list):
            tmp_img = tmp_img.from_tensor(tmp_tensor,docopy=False)
            tmp_imgs.append(tmp_img)
        self.data=tmp_imgs
            
        return ret_obj
    
    def from_tensor(self,tensor,docopy=True):
        return self.from_tensor_list(self,np.array_split(tensor,tensor.shape[0],0))
        
    
    def __getitem__(self,idx):
        return self.data[idx]
    
    def shape(self):
        return self.data[0].shape()
    
    def add_other_data(self,key,vals):
        for img,val in zip(self.data,vals):
            img.add_other_data(key,vals)
    
    
class GroupedImgLists(ImgCollection,
                      NestedImgCollection):
    def __init__(self,img_lists):
        assert(all([isinstance(x, ImgList) for x in img_lists]))
        self.data=img_lists
        self.myname=get_random_name()
        
    def _nodata_copy(self):
        return GroupedImgLists([tmp._nodata_copy() for tmp in self.data])
    
    def __len__(self):
        return len(self.data[0])
    
    def as_flat_lists(self):
        return [vl.as_flat_list() for vl in self.data]
        
    def as_ImgGroupList(self):
        return ImgGroupList([ImgGroup(list(x)) for x in zip(*[tmp.data for tmp in self.data])])
        
    def as_tensor(self):
        return [tmp.as_tensor() for tmp in self.data]
    
    def from_tensor_list(self,tensor_list,docopy=True):
        
        if(docopy):
            new_self=self._nodata_copy()
            new_self.data = [tmp.from_tensor_list(img_list,docopy=False) for tmp,img_list in zip(new_self.data,tensor_list)]
            retobj=new_self
        else:
            self.data = [tmp.from_tensor_list(img_list,docopy=False) for tmp,img_list in zip(self.data,tensor_list)]
            retobj=self
        return retobj
    
    def from_tensor(self,tensor_list,docopy=True):
        return self.from_tensor_list([np.array_split(tmp,tmp.shape[0],0) for tmp in tensor_list], docopy)
    
    def __getitem__(self,idx):
        return [tmp[idx] for tmp in self.data]

    def get_ImgGroup(self,idx):
        return ImgGroup(self[idx])
    
    def shape(self):
        return self.get_ImgGroup(0).shape()
    
    def num_views():
        return len(self.data)
    
    def add_other_data(self,key,valss):
        for imglist,vals in zip(self.data,valss):
            img.add_other_data(key,val)
    
class ImgGroupList(ImgCollection,
                   NestedImgCollection):
    def __init__(self,img_groups):
        assert(all([isinstance(x, ImgGroup) for x in img_groups]))
        self.data=img_groups
        self.myname=get_random_name()
        
    def __len__(self):
        return len(self.data)    
    
    def _nodata_copy(self):
        return ImgGroupList([tmp._nodata_copy() for tmp in self.data])
    
    def as_GroupedImgLists(self):
        return GroupedImgLists([list(x) for x in zip(*self.data)])
    
    def as_tensor(self):
        return self.as_GroupedImgLists.as_tensor()
    
    def from_tensor_list(self,tensor_list,docopy=True):
        
        if(docopy):
            new_self=self._nodata_copy().as_GroupedImgLists().from_tensor_list(tensor_list,do_copy=False).as_ImgGroupList()
        else:
            self = self.as_GroupedImgLists().from_tensor_list(tensor_list,do_copy=False).as_ImgGroupList()
        
        return self

    def from_tensor(self,tensor_list,docopy=True):
        return self.from_tensor_list([np.array_split(tmp,tmp.shape[0],0) for tmp in tensor_list], docopy)
    
    def __getitem__(self,idx):
        return self.data[idx]
    
    def shape(self):
        return self[0].shape()
    
    def num_views():
        return self.data[0].num_views()
    

    
class Video(ImgList,
            Offsettable,
            Paddable):
    def __init__(self,frames,video_path,frame_idxs,other_data=OrderedDict(),per_frame_extra_data=None):
        got_ndarray_list = all([isinstance(x, np.ndarray) for x in frames])
        got_Img_list = all([isinstance(x, Img) for x in frames])

        assert(got_ndarray_list or got_Img_list)
        
        frames_to_idxs_parity = len(frames)>=len(frame_idxs)

        
        assert(frames_to_idxs_parity)

        if not per_frame_extra_data is None:
            kwargs_supp = lambda tidx: {'other_data':per_frame_extra_data[tidx]}
        else:
            kwargs_supp = lambda tidx: {}

        if(got_ndarray_list):
            img_list=[]
            for idx,frame in enumerate(frames):
                if idx<len(frame_idxs):
                    frame_name=str(frame_idxs[idx])
                else:
                    frame_name='pad_'+str(idx)
                img_list.append(Img(frame, path=video_path+':'+frame_name,**(kwargs_supp(idx))))
        else:
            img_list=frames
            
        super(Video, self).__init__(img_list)
        
        self.video_path=video_path
        self.time_idxs=frame_idxs
        self.length=len(frame_idxs)
        self.other_data=other_data

    def is_padded(self):
        return len(frames)>len(frame_idxs)
    
    def sequence_length(self):
        return len(self.time_idxs)
        
    def _nodata_copy(self):
        retval = Video([tmp._nodata_copy() for tmp in self.data],
                     self.video_path,
                     self.time_idxs,
                     copy.deepcopy(self.other_data))
        return retval

class VideoGroup(GroupedImgLists,OffsettableCollection,PaddableCollection,NestedImgCollection):
    def __init__(self,videos):
        assert(all([isinstance(x, Video) for x in videos]))
        assert(all([v.length==videos[0].length for v in videos]))
        assert(all([v.time_idxs==videos[0].time_idxs for v in videos]))
        self.data=videos
        self.length=len(videos[0])
        self.myname=get_random_name()
    
    def num_views():
        return len(self.data)
    
    def __len__(self):
        return len(self.data[0])

    def sequence_length(self):
        return self.data[0].sequence_length()
        

class VideoList(SingleViewImgTree,
                OffsettableCollection,
                ImgCollection,
                PaddableCollection,
                NestedImgCollection):
    def __init__(self,videos,sequence_lengths=None):
        assert(all([isinstance(x, Video) for x in videos]))
        self.data=videos
        self.videos_paths=[vid.video_path for vid in videos]
        self.time_idxs=[vid.time_idxs for vid in videos]
        self.myname=get_random_name()
        if sequence_lengths is None:    
            self.init_sequence_lengths=[v.length for v in self.data]
        else:
            self.init_sequence_lengths=sequence_lengths
    
    def _nodata_copy(self):
        retval =  VideoList([v._nodata_copy() for v in self.data], self.sequence_lengths)
        return retval
    
    def __len__(self):
        return len(self.data)
    
    def shape(self):
        return self.data[0].shape()
    
    def join(self, *args):
        other_data=list(itertools.chain.from_iterable([tmp.data for tmp in args]))
        return VideoList(self.data+other_data)
        

    def sequence_lengths(self):
        return [tmp.sequence_length() for tmp in self.data]
    
    def as_tensor(self):
        img_list = ImgList(list(itertools.chain.from_iterable([v.data for v in self.data])))
        return img_list.as_tensor()
    
    def as_flat_list(self):
        img_list = ImgList(list(itertools.chain.from_iterable([v.data for v in self.data])))
        return img_list.as_flat_list()
    
    
    def from_tensor_list(self,tensor_list,docopy=True):
        if(docopy):
            new_self=self._nodata_copy()
            new_self.data = [tmp.from_tensor_list(img_list,docopy=False) for tmp,img_list in zip(new_self.data,tensor_list)]
            retobj=new_self
        else:
            self.data = [tmp.from_tensor_list(img_list,docopy=False) for tmp,img_list in zip(self.data,tensor_list)]
            retobj=self
        return retobj

    def from_tensor(self,tensor,padded_length=None,docopy=True):
        
        sequence_lengths=self.sequence_lengths()
        if not padded_length is None:
            splitpoints=np.cumsum([padded_length]*len(self.sequence_lengths()))
        else:
            splitpoints=np.cumsum(self.sequence_lengths())

        tensor_list=[np.array_split(tmp,tmp.shape[0],axis=0)[sequence_lengths[idx]] for idx,tmp in enumerate(np.split(tensor,splitpoints,axis=0))]
        return self.from_tensor_list(tensor_list,docopy=True)

    def __getitem__(self,idx):
        return self.data[idx]
        
    def add_other_data(self,key,valss):
        for imglist,vals in zip(self.data,valss):
            img.add_other_data(key,vals)
    

class VideoGroupList(OffsettableCollection,
                     ImgCollection,
                     PaddableCollection,
                     NestedImgCollection):
    def __init__(self,video_groups_list):
        assert(all([isinstance(x, VideoGroup) for x in video_groups_list])
               or all([all([(isinstance(tmp,Video)) for tmp in x]) for x in video_groups_list]))

        self.myname=get_random_name()
        self.data=video_groups_list
    
    def __len__(self):
        return len(self.data)

    def sequence_lengths(self):
        return [tmp.sequence_length() for tmp in self.data]
    
    def join(self, *args):
        other_data=list(itertools.chain.from_iterable([tmp.data for tmp in args]))
        return VideoGroupList(self.data+other_data)
        
        
    def as_ImgGroupList(self):
        new_data_list=[]
        for f in self.data:
            new_data_list+=f.as_ImgGroupList().data
        return ImgGroupList(new_data_list)
    
    def as_GroupedVideoLists(self):
        tmp_data=[tmp.data for tmp in self.data]
        reordered_videos=[VideoList(list(x)) for x in zip(*tmp_data)]
        return GroupedVideoLists(reordered_videos)
    
    def as_tensor(self):
        return self.as_GroupedVideoLists().as_tensor()
    
    def __getitem__(self,idx):
        return self.data[idx]
    
    def num_views():
        return self.data[0].num_views()
    
    def from_tensor_list(self,tensor_list,docopy=True):
        return self.as_GroupedVideoLists().from_tensor_list(tensor_list,docopy).as_VideoGroupList()
        
    def from_tensor(self,tensor_l,docopy=True):
        return self.as_GroupedVideoLists().from_tensor(tensor_l,docopy).as_VideoGroupList()
    
    
class GroupedVideoLists(MultiViewImgTree,
                        OffsettableCollection,
                        ImgCollection,
                        PaddableCollection,
                        NestedImgCollection):
    def __init__(self,video_lists):
        assert(all([isinstance(x, VideoList) for x in video_lists]))
        self.data=video_lists
        self.myname=get_random_name()
        
    def join(self,*args):
        return GroupedVideoLists([tmp2[0].join(*list(tmp2[1:])) for tmp2 in zip(self.data,*[tmp.data for tmp in args])])

    def as_ImageGroupList(self):
        pass

    def __len__(self):
        return len(self.data[0])
    
    def as_VideoGroupList(self):
        return VideoGroupList([VideoGroup(list(x)) for x in zip(*self.data)])
        
    def as_tensor(self):
        return [vl.as_tensor() for vl in self.data]

    def as_flat_lists(self):
        return [vl.as_flat_list() for vl in self.data]

    
    def __getitem__(self,idx):
        return VideoGroup([tmp[idx] for tmp in self.data])

    def _nodata_copy(self):
        retval = GroupedVideoLists([vl._nodata_copy() for vl in self.data])
        return retval

    def num_views(self):
        return len(self.data)
    
    def num_samps(self):
        return sum(self.sequence_lengths())
    
    def sequence_lengths(self):
        return self.data[0].sequence_lengths()
    
    def from_tensor_list(self,tensor_list,docopy=True):
        if(docopy):
            retobj=self._nodata_copy()
        else:
            retobj=self
        
        retobj.data = [tmp.from_tensor_list(img_list,docopy=False) for tmp,img_list in zip(retobj.data,tensor_list)]            
        return retobj

    def from_flat_tensor_list(self,tensor_l,padded_length=None,docopy=True):
        split_tls=[]
        
        sequence_lengths=self.sequence_lengths()
        if not padded_length is None:
            splitpoints=np.cumsum([padded_length]*len(self.sequence_lengths()))
        else:
            splitpoints=np.cumsum(self.sequence_lengths())
        
        splitpoints=splitpoints[:-1]
        for idx,tl in enumerate(tensor_l):
            split_tl=[tmp[:sequence_lengths[idx2]] for idx2,tmp in enumerate(list_split(tl,splitpoints))]
            split_tls.append(split_tl)
        return self.from_tensor_list(split_tls,docopy)


    def from_tensor(self,tensor_l,padded_length=None,docopy=True):
        split_tls=[]
        
        sequence_lengths=self.sequence_lengths()
        if not padded_length is None:
            splitpoints=np.cumsum([padded_length]*len(self.sequence_lengths()))
        else:
            splitpoints=np.cumsum(self.sequence_lengths())
        
        splitpoints=splitpoints[:-1]
        for idx,tl in enumerate(tensor_l):
            split_tl=[np.array_split(tmp,tmp.shape[0],axis=0)[:sequence_lengths[idx2]] for idx2,tmp in enumerate(np.split(tl,splitpoints,axis=0))]
            split_tls.append(split_tl)
        return self.from_tensor_list(split_tls,docopy)
        

    def shape(self):
        return [tmp.shape() for tmp in self.data]
    
        
    def add_other_data(self,key,valss):
        for vidlist,vals in zip(self.data,valss):
            vid.add_other_data(key,val)
    

def tests():
    squeezer=lambda x:[np.squeeze(tmp) for tmp in x]
    
    view1_clip1 = squeezer(np.array_split(np.arange(0,90).reshape((10,3,3)),10,0))
    view1_clip2 = squeezer(np.array_split(np.arange(1000,1180).reshape((20,3,3)),20,0))
    view1_clip3 = squeezer(np.array_split(np.arange(500,545).reshape((5,3,3)),5,0))

    view2_clip1 = squeezer(np.array_split(-1*np.arange(0,90).reshape((10,3,3)),10,0))
    view2_clip2 = squeezer(np.array_split(-1*np.arange(1000,1180).reshape((20,3,3)),20,0))
    view2_clip3 = squeezer(np.array_split(-1*np.arange(500,545).reshape((5,3,3)),5,0))
    
    
    vid_1_a = Video(view1_clip1, 'view1_clip1', range(0,10))
    vid_2_a = Video(view1_clip2, 'view1_clip2', range(50,70))
    vid_3_a = Video(view1_clip3, 'view1_clip3', range(100,105))
    
    vid_1_b = Video(view2_clip1, 'view2_clip1', range(0,10))
    vid_2_b = Video(view2_clip2, 'view2_clip2', range(50,70))    
    vid_3_b = Video(view1_clip3, 'view1_clip3', range(100,105))
    
    clip1=VideoGroup([vid_1_a,vid_1_b])
    clip2=VideoGroup([vid_2_a,vid_2_b])
    clip3=VideoGroup([vid_3_a,vid_3_b])
    
    grouptest=VideoList([vid_1_a,vid_2_a,vid_3_a])
    
    
    v_group_list=VideoGroupList([clip1,clip2])
    v_group_list2=VideoGroupList([clip3])    
    v_group_list3 = v_group_list.join(v_group_list2)
    
    v_group_list3_as_gv = v_group_list3.as_GroupedVideoLists()
    
    vidlist=v_group_list3_as_gv.data[0]
    
    assign_tensor_to_other_data(np.arange(0,35).reshape(35,1), 'rs', vidlist)
    vidlist.print_other_data('rs')
    gttest=fetch_from_other_data('rs', vidlist)
    
    gv_list=v_group_list.as_GroupedVideoLists()
    gv_list2=v_group_list2.as_GroupedVideoLists()
    gv_list3=gv_list.join(gv_list2)
    
    v_group_list_tensor=v_group_list3.as_tensor()
    
    clip1_as_imggrouplist=clip1.as_ImgGroupList()
    
    
    tmp=1
    
#tests()