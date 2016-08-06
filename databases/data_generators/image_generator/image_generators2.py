import os, time, copy, sys,threading, random,math,itertools,numpy as np
from scipy.misc import imread
from pathos.pools import ThreadPool
import menpo.io
from Queue import Queue

import sbpy_utils.core.sets
import sbpy_utils.core.string_manipulation as stringman
from sbpy_utils.core.list_tools import list_traverse_apply
from sbpy_utils.core.string_manipulation import concat_string_list,filter_empty_strings
from sbpy_utils.core.key_val import *
from sbpy_utils.core.command_line import my_system
import sbpy_utils.core.my_io
from sbpy_utils.core.chaining import apply_func_pipeline_masked,\
    apply_func_pipeline_masked_wrapped,add_to_masking_func_pipeline
from sbpy_utils.image.my_io import imread_safe
from media_types import Video,VideoGroup,VideoGroupList,GroupedVideoLists,Img,ImgList,ImgGroupList,GroupedImgLists


def get_grouped_image_generator3(folder, glob_matchers,grouper,use_cache_file,ban_files, ban_list, opts={}):

    igs = [];
    for i in range(0,len(glob_matchers)):
        ig = get_image_generator3(folder, glob_matchers[i],use_cache_file, ban_files[i], ban_list, opts);
        igs.append(ig);

        
    gig = GroupedImageGenerator3(igs);
    print('Grouping lists for GroupedImageGenerator3');
    
    if(len(glob_matchers)>1):
        grouped_image_generator = gig.group_lists(grouper);
    else:
        grouped_image_generator=gig;

    return grouped_image_generator


def get_grouped_video_generator3(folder, glob_matchers,grouper,use_cache_file,ban_files, ban_list, opts={}):

    igs = [];
    for i in range(0,len(glob_matchers)):
        if(len(ban_files)==1):
            bf=ban_files[0]
        else:
            bf=ban_files[i]
        
        ig = get_video_generator3(folder, glob_matchers[i],use_cache_file, bf, ban_list, opts);
        igs.append(ig);

    gig = GroupedVideoGenerator3(igs);
    print('Grouping lists for GroupedImageGenerator3');
    
    if(len(glob_matchers)>1):
        gig.group_lists(grouper);

    grouped_image_generator=gig;

    return grouped_image_generator

def get_video_generator3(folder, glob_matcher,use_cache_file, ban_file, ban_list, opts):


    if not use_cache_file:

        cmd = concat_string_list(['find',kv_get('follow_symlinks',opts,''),folder,'-wholename','"'+glob_matcher+'"'],' ')
        res = my_system(cmd)
        lines = res.split('\n')
    else:
        cache_file = kvg('file_list_cache',opts,os.path.join(folder,'file_list.txt'));
        regex_matcher=glob_matcher.replace('/','\/');
        regex_matcher=regex_matcher.replace('.','\.');
        regex_matcher='"'+regex_matcher.replace('*','.*')+'"'

        cmd = concat_string_list(['cat',cache_file,'|','ack',regex_matcher,'| sed -e "s/^.*$/&1\\\n/"'],' ');
        res = my_system(cmd);
        lines = res.split('1\n');

    lines = stringman.filter_empty_strings(lines);
    clean_lines = [line.strip() for line in lines]

    if( not ban_file=='' ):
        banned_images = filter_empty_strings(sbpy_utils.core.my_io.my_readlines(ban_file));
        cleaned_lines_banfree = list(set(clean_lines).difference(set(banned_images)))	
    else:
        cleaned_lines_banfree = clean_lines;

    if(len(ban_list)>0):
        cleaned_lines_banfree = stringman.multifilter_string_list(cleaned_lines_banfree,ban_list,1);

    image_generator = VideoGenerator3(cleaned_lines_banfree);
    return image_generator


def get_image_generator3(folder, glob_matcher,use_cache_file, ban_file, ban_list, opts):

 
    if not use_cache_file:
        
        cmd = concat_string_list(['find',kv_get('follow_symlinks',opts,''),folder,'-wholename','"'+glob_matcher+'"'],' ')
        res = my_system(cmd)
        lines = res.split('\n')
    else:
        cache_file = kvg('file_list_cache',opts,os.path.join(folder,'file_list.txt'));
        regex_matcher=glob_matcher.replace('/','\/');
        regex_matcher=regex_matcher.replace('.','\.');
        regex_matcher='"'+regex_matcher.replace('*','.*')+'"'
        
        cmd = concat_string_list(['cat',cache_file,'|','ack',regex_matcher,'| sed -e "s/^.*$/&1\\\n/"'],' ');
        res = my_system(cmd);
        lines = res.split('1\n');
        
    lines = stringman.filter_empty_strings(lines);
    clean_lines = [line.strip() for line in lines]
    
    if( not ban_file=='' ):
        banned_images = filter_empty_strings(sbpy_utils.core.my_io.my_readlines(ban_file));
        cleaned_lines_banfree = list(set(clean_lines).difference(set(banned_images)))	
    else:
        cleaned_lines_banfree = clean_lines;
    
    
    if(len(ban_list)>0):
        cleaned_lines_banfree = stringman.multifilter_string_list(cleaned_lines_banfree,ban_list,1);
    


    image_generator = ImageGenerator3(cleaned_lines_banfree);
    return image_generator

class GroupedImageGenerator3:


    def __init__(self, image_generators):
        self.file_lists=[]
        for i in range(0,len(image_generators)):
            if(isinstance(image_generators[i], ImageGenerator3)):
                self.file_lists.append(image_generators[i].file_list);
            elif(isinstance(image_generators[i],list)):
                self.file_lists.append(image_generators[i]);
            else:
                raise TypeError('You can only make a GroupedImageGenerator3 from a list of string-lists or ImageGenerator2s')
            
            self.file_lists[i] = filter(None,self.file_lists[i]);

        self.imreader_callback = imread_safe;
        self.ctr = 1;
        self.enable_caching=0;
        self.enable_pp_caching=0;

        self.modification_pipelines={}
        self.structured_modification_pipelines={}

        self.img_pp_cache={}
        self.img_pp_oo_cache={}
        self.img_cache={}
        self.opts={}

    def group_lists(self,get_key_callback):
        new_file_lists=sbpy_utils.core.sets.group_by(self.file_lists,get_key_callback);
        self.file_lists=new_file_lists;


    def dynamic_func(self,key,*args):
        fhandle = self.opts[key];
        out = fhandle(*args);
        return out

    def has_next(self):
        return self.ctr<len(self.file_lists[1])
    
    def reset(self):
        self.ctr=1
    
                    
    def next(self):
                
        [self, imgs] = self.peek();
        self = self.increment();
        return (imgs)

    
    def get_sample_dims(self, pipeline_mask=[], invert_pipeline_mask=True):
                
        imgs=[]
        for i in range(0,len(self.file_lists)):
            img_path = self.file_lists[i][self.ctr];
            img = self.imreader_callback(img_path.strip());
            
            modified_img = apply_func_pipeline_masked(img, self.modification_pipelines[i], pipeline_mask, invert_pipeline_mask);
            
            imgs.append(modified_img)
        
        dims = [x.shape for x in imgs];
        return dims
    
                
            
    def get(self, idx, pipeline_mask=[], invert_pipeline_mask=True):
        imgs=[]
        img_paths=[]
        #print('GroupedImageGenerator3');
        for i in range(0,len(self.file_lists)):
            mij_path = self.file_lists[i][idx].strip();
            
            if(self.enable_caching and (mij_path in self.img_cache)):
                img = self.img_cache[mij_path];
                #print(mij_path+'(using cache) ; ')
            elif(self.enable_caching and (not mij_path in self.img_cache)):
                img = self.imreader_callback(mij_path);
                self.img_cache[mij_path]=img
                #print(mij_path + '(caching) ; ');
            else:
                img = self.imreader_callback(mij_path);
                #print(mij_path+' ; ');
            
           
            pp_cache_key=stringman.sanitize_string(mij_path+str(pipeline_mask)+str(invert_pipeline_mask));
            if(self.enable_pp_caching and kv_haskey(pp_cache_key,self.img_pp_cache)):
                modified_img = self.img_pp_cache[pp_cache_key];
                #print(mij_path+'(using img_pp_cache) ; ');
            elif(self.enable_pp_caching and not (pp_cache_key in self.img_pp_cache)):
                modified_img = apply_func_pipeline_masked(img, self.modification_pipelines[i], pipeline_mask, invert_pipeline_mask);
                self.img_pp_cache = kv_set(pp_cache_key,modified_img,self.img_pp_cache);
                #print([mij_path,'(caching to img_pp_cache) ; ']);
            else:
                modified_img = apply_func_pipeline_masked(img, self.modification_pipelines[i], pipeline_mask, invert_pipeline_mask);
                #print([mij_path,' ; ']);
            
            
            imgs.append(Img(data=modified_img, path=mij_path,other_data=OrderedDict({'sample_idx':idx})));
            
        
        return ImgGroup(imgs)
    
    
    def start_fill(self,batchsize,sample_idxs_getter,io_pool,queuesize=10,pipeline_mask=[], invert_pipeline_mask=True):
        self.read_queue = Queue(maxsize=queuesize)
        self.worker_threads_events=[]
        self.worker_threads=[]
        def structured_gets_loop(queue_obj,event_obj,thr_io_pool):
            while True:
                samples_idxs=sample_idxs_getter()
                grouped_image_lists = self.structured_gets(samples_idxs, thr_io_pool, pipeline_mask, invert_pipeline_mask)
                queue_obj.put( grouped_image_lists )
                event_is_set = event_obj.wait()
 
        num_threads=1
        
        for i in range(num_threads):
            worker_event = threading.Event()
            worker_event.set()
            worker = threading.Thread(target=structured_gets_loop, args=(self.read_queue,worker_event,io_pool))
            worker.setDaemon(True)
            self.worker_threads.append(worker)
            self.worker_threads_events.append(worker_event)
            worker.start()
        
    def structured_gets_from_q(self):
        res=self.read_queue.get()
        rq=self.read_queue
        item_consumed_handle = rq.task_done
        return (res,item_consumed_handle)
        
    
    def pause_fill(self):
        for event_obj in self.worker_threads_events:
            event_obj.clear()
        with self.read_queue.mutex:
            self.read_queue.queue.clear()        
    
    def resume_fill(self):
        for event_obj in self.worker_threads_events:
            event_obj.set()    

    def gets(self, idxs, io_pool, pipeline_mask=[], invert_pipeline_mask=True):
        f = lambda idx: self.get(idx, pipeline_mask, invert_pipeline_mask)
        data_objs_tmp = io_pool.map(f,idxs)
        tmp_img_group_list=ImgGroupList(data_objs_tmp)
        return tmp_img_group_list.as_GroupedImgLists()
    
    def structured_gets(self, idxs, io_pool, pipeline_mask=[], invert_pipeline_mask=True):
        f = lambda idx: self.stuctured_get(idx, pipeline_mask, invert_pipeline_mask)
        data_objs_tmp = io_pool.map(f,idxs)
        tmp_img_group_list=ImgGroupList(data_objs_tmp)
        return tmp_img_group_list.as_GroupedImgLists()
               
    def structured_get(self,*args):
        return self.stuctured_get(*args)
    
    def stuctured_get(self, idx, pipeline_mask=[], invert_pipeline_mask=True):

        img_paths=[]
        imgs=[]
        pipeline_oos=[];
        #print('GroupedImageGenerator3');
        for i in range(0,len(self.file_lists)):
            mij_path = self.file_lists[i][idx].strip()
            #print(mij_path)
            
            if(self.enable_caching and self.img_cache[mij_path]):
                img = self.img_cache[mij_path];
                #print(mij_path+'(using cache) ; ');
            elif(self.enable_caching and not self.img_cache[mij_path]):
                img = self.imreader_callback(mij_path);
                self.img_cache[mij_path] = img
                #print(mij_path+'(caching) ; ')
            else:
                img = self.imreader_callback(mij_path);
                #print(mij_path+' ; ');
            
            pipeline_mask_str={True:'emptypipelinemask',False:str(pipeline_mask)}[pipeline_mask==[]];
            pp_cache_key=stringman.sanitize_string(os.path.join(mij_path, pipeline_mask_str, 'ipm_'+str(invert_pipeline_mask)));
            if(self.enable_pp_caching and (pp_cache_key in self.img_pp_cache)):
                modified_img = self.img_pp_cache[pp_cache_key];
                oo = self.img_pp_oo_cache[pp_cache_key]
                #print(mij_path+'(using img_pp_cache) ; ');
            elif(self.enable_pp_caching and not (pp_cache_key in self.img_pp_cache)):
                chain_res = chain.apply_func_pipeline_masked_wrapped(img, self.structured_modification_pipelines[i], pipeline_mask, invert_pipeline_mask);
                modified_img=chain_res[0]
                oo=chain_res[1]
                elf.img_pp_cache[pp_cache_key] = modified_img
                self.img_pp_oo_cache[pp_cache_key] = oo
                #print(mij_path+'(caching to img_pp_cache) ; ')
            else:
                chain_res = apply_func_pipeline_masked_wrapped(img, self.structured_modification_pipelines[i], pipeline_mask, invert_pipeline_mask);
                modified_img=chain_res[0]
                oo=chain_res[1]
                #print(mij_path+' ; ');
            
            new_img_obj=Img(data=modified_img, path=mij_path, other_data=oo)
            imgs.append(new_img_obj);
        return ImgGroup(imgs)

    def set_image_reader(self, imreader_callback):
        self.imreader_callback = imreader_callback
    
    def peek(self):
        return(self.get(self.ctr))
        
    def increment(self):
        self.ctr+=1;
    
    def set_image_modifiers(self,modification_pipelines):
        self.modification_pipelines=modification_pipelines;
    
    def set_structured_image_modifiers(self,structured_modification_pipelines):
        self.structured_modification_pipelines=structured_modification_pipelines;
    
    def get_func_pipeline(self):
        return copy.deepcopy(self.modification_pipelines);
    
    def get_structured_func_pipeline(self):
        return copy.deepcopy(self.structured_modification_pipelines)

    def get_num_samples(self):
        return len(self.file_lists[0]);
    
    def get_num_groups(self):
        return len(self.file_lists);

class ImageGenerator3:
    
    def __init__(self,file_list, modification_pipeline=None):
        self.file_list=file_list;
        self.ctr = 1;
        self.imreader_callback = imread_safe;
        if not modification_pipeline is None: 
            self.modification_pipeline=modification_pipeline
     
    def reset(self):
        self.ctr=1
    
    def increment(self):
        self.ctr+=1
    
    def set_image_modifiers(self,modification_pipeline):
        self.modification_pipeline=modification_pipeline
    
    def get_sample_dims(self):
        
        img_path = self.file_list[1];
        img = self.imreader_callback(strtrim(img_path));
        modified_img = chain.apply_func_pipeline_masked(img, self.modification_pipeline);
        dims = modified_img.shape;
        return dims
     
    def get(self, idx):
        
        img_path = self.file_list[idx].strip();
        raw_img = self.imreader_callback(img_path);
        img = chain.apply_func_pipeline_masked(raw_img, self.modification_pipeline);
        return Img(data=img, path=img_path)
    
    def next(self):
        
        res = self.peek();
        self.increment();
        return (img, img_path)
        
    def get_num_samples(self):
        return len(self.file_list);
    
    def peek(self):
        return self.get(self.ctr);
    
    def set_image_reader(self, imreader_callback):
        self.imreader_callback = imreader_callback;
    
    def has_next(self):
        return self.ctr<length(self.file_list);
    
def menpo_import_video_verbose(vp):
    print('menpo.io.import_video importing %s' % vp)
    try:
        return (menpo.io.import_video(vp, 
                                      exact_frame_count=False, 
                                      normalise=False))
    except Exception as err:
        print('menpo.io.import_video could not import %s' % vp)
        print(err)
        return None



class VideoGenerator3():
    def __init__(self,file_list, modification_pipeline=None, use_menpo_type=False):
        videos=OrderedDict()
        file_list_filtered=[]
        
        video_getter_pool=ThreadPool(nodes=8)
        mpio_obj_list = video_getter_pool.map(menpo_import_video_verbose,file_list)
        
        for vp,mpio_obj in zip(file_list,mpio_obj_list):
            if not mpio_obj is None:
                videos[vp]=mpio_obj
                file_list_filtered.append(vp)
        
        #for vp in file_list:
            #print('menpo.io.import_video importing %s' % vp)
            #try:
                #mpio_obj=menpo.io.import_video(vp, exact_frame_count=False, normalise=False)
                #videos[vp]=mpio_obj
            #except Exception as err:
                #print('menpo.io.import_video could not import %s' % vp)
                #print(err)
                
        self.file_list = file_list_filtered    
        self.videos=videos
        if not modification_pipeline is None:
            self.modification_pipeline=modification_pipeline
        self.fps=mpio_obj.fps
        self.use_menpo_type=use_menpo_type

    def set_image_modifiers(self,modification_pipeline):
        self.modification_pipeline=modification_pipeline
    
    def get_sample_dims(self):
        modified_img=self.get(1)
        dims = modified_img.shape;
        return dims
     
    def get(self, idx, time_idxs):
        if(isinstance(idx, str) ):
            vid_path=idx
        elif(isinstance(idx,int)):
            vid_path = self.videos.keys()[idx]
        else:
            raise TypeError('idx must be int or string')

        lazy_frame_list=self.videos[vid_path]
        sliced_frame_list=lazy_frame_list[time_idxs]
        
        img_type_converter = lambda x:x if self.use_menpo_type else menpo_to_rgb
        
        processed_imgs=[None]*len(sliced_frame_list)
        for frame_idx,frame in enumerate(sliced_frame_list):
            processed_img = apply_func_pipeline_masked(img_type_converter(frame), self.modification_pipeline);
            processed_imgs[frame_idx]=processed_img        
        return Video(processed_imgs, video_path=vid_path, frame_idxs=time_idxs)
        
    
    def get_random_segment(self,min_length=3,alpha=12,beta=0.5):
        file_idx=random.randint(0,len(self.videos.keys())-1)
        vid_path=self.videos.keys()[file_idx]
        vid_length=len(self.videos[vid_path])
        start_idx=random.randint(0, vid_length-min_length)
        segment_length=max(random.gammavariate(alpha,beta),min_length)*self.videos[vid_path].fps
        end_idx=int(np.round(start_idx+segment_length))
        time_idxs=range(start_idx,end_idx)
        processed_segment = self.get(vid_path, time_idxs)
        return processed_segment
    

class GroupedVideoGenerator3:


    def __init__(self, 
                 image_generators=[],
                 fps=None,
                 modification_pipelines=None,
                 structured_modification_pipelines=None,
                 use_menpo_type=False,
                 opts={}):
        self.video_lists=[]
        self.file_lists=[]
        print('GroupedVideoGenerator3()')
        for i in range(0,len(image_generators)):
            if(isinstance(image_generators[i], VideoGenerator3)):
                assert(isinstance(image_generators[i].videos, OrderedDict))
                self.file_lists.append(image_generators[i].file_list);
                self.video_lists.append(image_generators[i].videos)
                fps=image_generators[i].fps
            elif(isinstance(image_generators[i],list)):
                video_getter_pool=ThreadPool(nodes=8)                
                tmp_mpio_obj_list=video_getter_pool.map(menpo_import_video_verbose, image_generators[i])
                tmp_mpio_obj_list = [x for x in tmp_mpio_obj_list if x is not None]
                safe_idxs = [idx for idx,x in enumerate(tmp_mpio_obj_list) if x is not None]
                tmp_file_list=image_generators[i]
                self.file_lists.append([tmp_file_list[safe_idx] for safe_idx in safe_idxs])                
                self.video_lists.append(tmp_mpio_obj_list)
            else:
                raise TypeError('You can only make a GroupedImageGenerator2 '+\
                                'from a list of string-lists or ImageGenerator2s')
            
            self.file_lists[i] = [tmp for tmp in self.file_lists[i] if not tmp is None]
        
        self.fps=fps
        self.modification_pipelines= \
            modification_pipelines if not modification_pipelines is None else {}
        self.structured_modification_pipelines= \
            structured_modification_pipelines if not structured_modification_pipelines is None else {}
        self.io_pool = None
        self.enable_caching = 0
        self.enable_pp_caching = 0
        self.img_pp_cache = {}
        self.img_pp_oo_cache = {}
        self.img_cache = {}
        self.opts = opts
        self.use_menpo_type = use_menpo_type
        
    def copy3(self):
        ret_val=GroupedVideoGenerator3([],
                                       fps=self.fps,
                                       modification_pipelines=self.modification_pipelines,
                                       structured_modification_pipelines=self.structured_modification_pipelines,
                                       use_menpo_type=self.use_menpo_type,
                                       opts=self.opts)
        ret_val.file_lists = copy.copy(self.file_lists)
        ret_val.video_lists = copy.copy(self.video_lists)
        return ret_val
        
    def group_lists(self,get_key_callback):
        
        new_file_lists=sbpy_utils.core.sets.group_by(self.file_lists,get_key_callback);
        self.file_lists=new_file_lists;
        
        reordered_video_lists=[]
        old_video_lists=self.video_lists
        
        for view_idx,file_list in enumerate(new_file_lists):
            reordered_video_list=OrderedDict()
            old_video_list=old_video_lists[view_idx]
            for g in file_list:
                reordered_video_list[g]=old_video_list[g]
                
    def dynamic_func(self,key,*args):
        fhandle = self.opts[key];
        out = fhandle(*args);
        return out    
                       
    def get_sample_dims(self, pipeline_mask=[], invert_pipeline_mask=True):
        vidgroup_obj=self.get(0,0,pipeline_mask, invert_pipeline_mask)
        return vidgroup_obj.shape()
        
    def structured_get(self, idx, time_idxs, pipeline_mask=[], invert_pipeline_mask=True): 
        return self._get(idx, time_idxs, pipeline_mask, invert_pipeline_mask,collect_pipeline_multi_outputs=True)
    
    def get(self, idx, time_idxs, pipeline_mask=[], invert_pipeline_mask=True):
        return self._get(idx, time_idxs, pipeline_mask, invert_pipeline_mask,collect_pipeline_multi_outputs=False)
    
    def get_num_samples(self):
        return len(self.file_lists[0]);
    

    def _get(self, idx, time_idxs, pipeline_mask=[], invert_pipeline_mask=True,collect_pipeline_multi_outputs=False):
        segments=[]
        metadatas=[]
        all_oos=[]
        
        if isinstance(time_idxs, int):
            time_idxs=[time_idxs]        
        
        img_type_converter = (lambda x:x) if self.use_menpo_type else menpo_to_rgb
        
        for i in range(0,len(self.file_lists)):

            vid_path = self.video_lists[i].keys()[idx]
            video_obj = self.video_lists[i][vid_path]
    
    
            safe_time_idxs=[safe_idx for safe_idx in time_idxs if safe_idx <len(video_obj)]
            sliced_frame_list=video_obj[safe_time_idxs]
            
            if self.io_pool is None:
                
                processed_imgs=[]
                pipeline_oos=[]
                for frame in sliced_frame_list:
                    if collect_pipeline_multi_outputs:
                        processed_img,oo=apply_func_pipeline_masked_wrapped(img_type_converter(frame), self.structured_modification_pipelines[i],pipeline_mask, invert_pipeline_mask)
                        pipeline_oos.append(oo)
                        processed_imgs.append(processed_img)
                    else:
                        processed_img = apply_func_pipeline_masked(img_type_converter(frame), self.modification_pipelines[i],pipeline_mask, invert_pipeline_mask)
                        processed_imgs.append(processed_img)
            else:
                if collect_pipeline_multi_outputs:
                    frame_proc = lambda frame: apply_func_pipeline_masked_wrapped(img_type_converter(frame), self.structured_modification_pipelines[i],pipeline_mask, invert_pipeline_mask)     
                    processed_imgs_oos = self.io_pool.map(frame_proc,sliced_frame_list)
                    processed_imgs,pipeline_oos=zip(*processed_imgs_oos)
                else:
                    frame_proc = lambda frame: apply_func_pipeline_masked(img_type_converter(frame), self.modification_pipelines[i],pipeline_mask, invert_pipeline_mask)
                    processed_imgs = self.io_pool.map(frame_proc,sliced_frame_list)
                
            #if(self.enable_caching and (mij_path in self.img_cache)):
                #img = self.img_cache[mij_path];
                ##print(mij_path+'(using cache) ; ')
            #elif(self.enable_caching and (not mij_path in self.img_cache)):
                #img = self.imreader_callback(mij_path);
                #self.img_cache[mij_path]=img
                ##print(mij_path + '(caching) ; ');
            #else:
                #img = self.imreader_callback(mij_path);
                ##print(mij_path+' ; ');
            
           
            #pp_cache_key=stringman.sanitize_string(mij_path+str(pipeline_mask)+str(invert_pipeline_mask));
            #if(self.enable_pp_caching and kv_haskey(pp_cache_key,self.img_pp_cache)):
                #modified_img = self.img_pp_cache[pp_cache_key];
                ##print(mij_path+'(using img_pp_cache) ; ');
            #elif(self.enable_pp_caching and not (pp_cache_key in self.img_pp_cache)):
                #modified_img = apply_func_pipeline_masked(img, self.modification_pipelines[i], pipeline_mask, invert_pipeline_mask);
                #self.img_pp_cache = kv_set(pp_cache_key,modified_img,self.img_pp_cache);
                ##print([mij_path,'(caching to img_pp_cache) ; ']);
            #else:
                #modified_img = apply_func_pipeline_masked(img, self.modification_pipelines[i], pipeline_mask, invert_pipeline_mask);
                ##print([mij_path,' ; ']);
            if collect_pipeline_multi_outputs:
                per_frame_extra_data=pipeline_oos
            else:
                per_frame_extra_data=None
                
            new_vid_obj=Video(processed_imgs, video_path=vid_path, frame_idxs=safe_time_idxs, per_frame_extra_data=per_frame_extra_data)
            segments.append(new_vid_obj);
        
        return VideoGroup(segments)
    
    def start_fill(self,queuesize=10,pipeline_mask=[],invert_pipeline_mask=True,min_length=3,max_length=5,alpha=12,beta=0.5):
        
        self.read_queue = Queue(maxsize=queuesize)
        self.worker_threads_events=[]
        self.worker_threads=[]
        def structured_get_loop(queue_obj,event_obj):
            while True:
                grouped_video_lists = self.get_random_segment_group(pipeline_mask, invert_pipeline_mask,min_length,max_length,alpha,beta)
                queue_obj.put( grouped_video_lists )
                event_is_set = event_obj.wait()
 
        num_threads=1
        for i in range(num_threads):
            worker_event = threading.Event()
            worker_event.set()
            worker = threading.Thread(target=structured_get_loop, args=(self.read_queue,worker_event))
            worker.setDaemon(True)
            self.worker_threads.append(worker)
            self.worker_threads_events.append(worker_event)
            worker.start()
        
    def get_random_segment_group_from_q(self,num_items=1):
        return self.structured_gets_from_q(num_items)
        
    def structured_gets_from_q(self,num_items=1):
        video_groups=[]
        for i in range(0,num_items):
            video_group=self.read_queue.get()
            video_groups.append(video_group)
        
        return (VideoGroupList(video_groups).as_GroupedVideoLists(),[self.read_queue.task_done]*num_items)

    def structured_get_from_q(self):
        return self.structured_gets_from_q()
    
    def pause_fill(self):
        for event_obj in self.worker_threads_events:
            event_obj.clear()
        with self.read_queue.mutex:
            self.read_queue.queue.clear()        
    
    def resume_fill(self):
        for event_obj in self.worker_threads_events:
            event_obj.set()    

    def gets(self, idxs, time_idxs_s, io_pool, pipeline_mask=[], invert_pipeline_mask=True):
        f = lambda idx,time_idxs: self.get(idx, time_idxs,pipeline_mask, invert_pipeline_mask)
        data_objs = io_pool.map(f,idxs,time_idxs_s)
        return data_objs
    
    def structured_gets(self, idxs, time_idxs_s, io_pool, pipeline_mask=[], invert_pipeline_mask=True):
        f = lambda idx, time_idx: self.structured_get(idx, time_idxs, pipeline_mask, invert_pipeline_mask)
        video_group_list = io_pool.map(f,idxs,time_idxs_s)
        return video_group_list.as_GroupedVideoLists()
    
    def get_random_segment_group(self,pipeline_mask=[], invert_pipeline_mask=True,min_length=3,max_length=5,alpha=12,beta=0.5):
        file_group_idx=random.randint(0,len(self.video_lists[0].keys())-1)
        vid_paths=[vlist[file_group_idx] for vlist in self.file_lists]
        
        vid_lengths=map(lambda vlist,path: len(vlist[path]), self.video_lists, vid_paths)
        vid_length=min(vid_lengths)
        start_idx=random.randint(0, vid_length-min_length)
        segment_length=min(max_length,max(random.gammavariate(alpha,beta),min_length))*self.fps
        end_idx=int(np.round(start_idx+segment_length))
        time_idxs=range(start_idx,end_idx)
        #print('intended_segment length: '+str(len(time_idxs)))
        processed_segment = self.structured_get(file_group_idx,time_idxs,pipeline_mask,invert_pipeline_mask)
        print('processed_segment length: '+str(len(processed_segment)))
        return processed_segment
    
               
    def set_image_modifiers(self,modification_pipelines):
        self.modification_pipelines=modification_pipelines;
    
    def set_structured_image_modifiers(self,structured_modification_pipelines):
        self.structured_modification_pipelines=structured_modification_pipelines;
    
    def get_func_pipeline(self):
        return copy.deepcopy(self.modification_pipelines);
    
    def get_structured_func_pipeline(self):
        return copy.deepcopy(self.structured_modification_pipelines)
    
    def get_num_groups(self):
        return len(self.file_lists);

    def init_thread_pool(self):
        self.io_pool=ThreadPool(nodes=4)

    def close_thread_pool(self): 
        self.io_pool.close()
    
def menpo_to_rgb(img_obj):
    return np.squeeze(np.moveaxis(img_obj.pixels,0,2))

def disp_image_sequence(*args):
    import matplotlib.pyplot as plt
    img = None
    
    seq_lengths=map(len,args)
    assert(all([seq_length==seq_lengths[0] for seq_length in seq_lengths]))
    
    for f in range(0,seq_lengths[0]):
        im_group=[tmp[f] for tmp in args]
        im = np.concatenate(tuple(im_group), axis=1)
        
        if img is None:
            img = plt.imshow(im,interpolation='nearest',animated=True, cmap = plt.get_cmap('gray'))
        else:
            img.set_data(im)
        plt.pause(.000000001)
        plt.draw()
    plt.close()
    

def test_VideoGenerator3():
    modification_pipeline=OrderedDict()
    modification_pipeline['grayscaler']=lambda x:x.as_greyscale()
    modification_pipeline['resizer']=lambda x:x.zoom(2.0)
    modification_pipeline['pixels']=lambda x:menpo_to_rgb(x)
    test_obj=VideoGenerator3(['/Users/sanjay/Movies/out100.mp4'], modification_pipeline=modification_pipeline,use_menpo_type=True)
    test_obj2=VideoGenerator3(['/Users/sanjay/Movies/out100.mp4'], modification_pipeline=modification_pipeline,use_menpo_type=True)
    
    test_obj3=GroupedVideoGenerator3([test_obj,test_obj2], 
                                     modification_pipelines=[copy.deepcopy(test_obj.modification_pipeline) for i in range(0,2)], 
                                     structured_modification_pipelines=[kv_apply(copy.deepcopy(test_obj.modification_pipeline),
                                               lambda tmp: {'func_handle':tmp,'output_keys':['operand']}) 
                                      for i in range(0,2)],use_menpo_type=True)
    random_seg_group=test_obj3.get_random_segment_group(min_length=10)
    random_seg_group.data[0]=random_seg_group.data[0].offset(5)
    random_seg_group.data[1]=random_seg_group.data[1].offset(-5)
    disp_image_sequence(*list_traverse_apply([rs for rs in random_seg.as_nested_list()],lambda x:x.pixels()))
    tmp=1
    
#test_VideoGenerator3()



