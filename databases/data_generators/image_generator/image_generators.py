import os, time, copy, sys
from scipy.misc import imread
import sbpy_utils.core.sets
import numpy as np
import sbpy_utils.core.string_manipulation as stringman
from sbpy_utils.core.string_manipulation import concat_string_list,filter_empty_strings
from sbpy_utils.core.key_val import *
from sbpy_utils.core.command_line import my_system
import sbpy_utils.core.my_io
from sbpy_utils.core.chaining import *
from sbpy_utils.image.my_io import imread_safe



def get_grouped_image_generator2(folder, glob_matchers,grouper,use_cache_file,ban_files, ban_list, opts={}):

    igs = [];
    for i in range(0,len(glob_matchers)):
        ig = get_image_generator(folder, glob_matchers[i],use_cache_file, ban_files[i], ban_list, opts);
        igs.append(ig);

        
    gig = GroupedImageGenerator2(igs);
    print('Grouping lists for GroupedImageGenerator2');
    
    if(len(glob_matchers)>1):
        grouped_image_generator = gig.group_lists(grouper);
    else:
        grouped_image_generator=gig;

    return grouped_image_generator

def get_image_generator(folder, glob_matcher,use_cache_file, ban_file, ban_list, opts):

 
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
    


    image_generator = ImageGenerator(cleaned_lines_banfree);
    return image_generator

class GroupedImageGenerator2:


    def __init__(self, image_generators):
        self.file_lists=[]
        for i in range(0,len(image_generators)):
            if(isinstance(image_generators[i], ImageGenerator)):
                self.file_lists.append(image_generators[i].file_list);
            elif(isinstance(image_generators[i],list)):
                self.file_lists.append(image_generators[i]);
            else:
                raise TypeError('You can only make a GroupedImageGenerator2 from a list of string-lists or ImageGenerator2s')
            
            self.file_lists[i] = filter(None,self.file_lists[i]);

        self.imreader_callback = imread_safe;
        self.ctr = 1;
        self.enable_caching=0;
        self.enable_pp_caching=0;
        self.opts={};    


        self.modification_pipelines={}
        self.structured_modification_pipelines={}

        self.img_pp_cache={}
        self.img_pp_oo_cache={}
        self.img_cache={}
        self.opts={}

    def group_lists(self,get_key_callback):
        new_file_lists=sbmat_core.sets.group_by(self.file_lists,get_key_callback);
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
                
        [self, imgs, img_paths] = self.peek();
        self = self.increment();
        return (imgs,imgs_paths)

    
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
        print('GroupedImageGenerator2');
        for i in range(0,len(self.file_lists)):
            mij_path = self.file_lists[i][idx].strip();
            
            if(self.enable_caching and (mij_path in self.img_cache)):
                img = self.img_cache[mij_path];
                print(mij_path+'(using cache) ; ')
            elif(self.enable_caching and (not mij_path in self.img_cache)):
                img = self.imreader_callback(mij_path);
                self.img_cache[mij_path]=img
                print(mij_path + '(caching) ; ');
            else:
                img = self.imreader_callback(mij_path);
                print(mij_path+' ; ');
            
           
            pp_cache_key=stringman.sanitize_string(mij_path+str(pipeline_mask)+str(invert_pipeline_mask));
            if(self.enable_pp_caching and kv_haskey(pp_cache_key,self.img_pp_cache)):
                modified_img = self.img_pp_cache[pp_cache_key];
                print(mij_path+'(using img_pp_cache) ; ');
            elif(self.enable_pp_caching and not (pp_cache_key in self.img_pp_cache)):
                modified_img = apply_func_pipeline_masked(img, self.modification_pipelines[i], pipeline_mask, invert_pipeline_mask);
                self.img_pp_cache = kv_set(pp_cache_key,modified_img,self.img_pp_cache);
                print([mij_path,'(caching to img_pp_cache) ; ']);
            else:
                modified_img = apply_func_pipeline_masked(img, self.modification_pipelines[i], pipeline_mask, invert_pipeline_mask);
                print([mij_path,' ; ']);
            
            imgs.append(modified_img);
            img_paths.append(mij_path);
        return (imgs, img_paths)
    
    
    def gets(self, idxs, io_pool, pipeline_mask=[], invert_pipeline_mask=True):
        f = lambda idx: self.get(idx, pipeline_mask, invert_pipeline_mask)
        data_objs = io_pool.map(f,idxs)
        return data_objs
    
    def structured_gets(self, idxs, io_pool, pipeline_mask=[], invert_pipeline_mask=True):
        f = lambda idx: self.stuctured_get(idx, pipeline_mask, invert_pipeline_mask)
        data_objs_tmp = io_pool.map(f,idxs)        
        
        data_obj_tmp,data_paths_tmp,data_obj_oos_tmp = [list(c) for c in zip(*data_objs_tmp)]
        
        data_obj,data_paths,data_obj_oos=[list(x) for x in zip(*data_obj_tmp)],[list(x) for x in zip(*data_paths_tmp)],[list(x) for x in zip(*data_obj_oos_tmp)]
        
        
        return (data_obj,data_paths,data_obj_oos)
               
    def stuctured_get(self, idx, pipeline_mask=[], invert_pipeline_mask=True):

        img_paths=[]
        imgs=[]
        pipeline_oos=[];
        print('GroupedImageGenerator');
        for i in range(0,len(self.file_lists)):
            mij_path = self.file_lists[i][idx].strip()
        
            
            if(self.enable_caching and self.img_cache[mij_path]):
                img = self.img_cache[mij_path];
                print(mij_path+'(using cache) ; ');
            elif(self.enable_caching and not self.img_cache[mij_path]):
                img = self.imreader_callback(mij_path);
                self.img_cache[mij_path] = img
                print(mij_path+'(caching) ; ')
            else:
                img = self.imreader_callback(mij_path);
                print(mij_path+' ; ');
            
            
            
            pipeline_mask_str={True:'emptypipelinemask',False:str(pipeline_mask)}[pipeline_mask==[]];
            pp_cache_key=stringman.sanitize_string(os.path.join(mij_path, pipeline_mask_str, 'ipm_'+str(invert_pipeline_mask)));
            if(self.enable_pp_caching and (pp_cache_key in self.img_pp_cache)):
                modified_img = self.img_pp_cache[pp_cache_key];
                oo = self.img_pp_oo_cache[pp_cache_key]
                print(mij_path+'(using img_pp_cache) ; ');
            elif(self.enable_pp_caching and not (pp_cache_key in self.img_pp_cache)):
                chain_res = chain.apply_func_pipeline_masked_wrapped(img, self.structured_modification_pipelines[i], pipeline_mask, invert_pipeline_mask);
                modified_img=chain_res[0]
                oo=chain_res[1]
                elf.img_pp_cache[pp_cache_key] = modified_img
                self.img_pp_oo_cache[pp_cache_key] = oo
                print(mij_path+'(caching to img_pp_cache) ; ')
            else:
                chain_res = apply_func_pipeline_masked_wrapped(img, self.structured_modification_pipelines[i], pipeline_mask, invert_pipeline_mask);
                modified_img=chain_res[0]
                oo=chain_res[1]
                print(mij_path+' ; ');
            

            
            pipeline_oos.append(oo);
            imgs.append(modified_img);
            img_paths.append(mij_path);
        
        print('\n');

        return (imgs, img_paths, pipeline_oos)



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

class ImageGenerator:
    
    def __init__(self,file_list):
        self.file_list=file_list;
        self.ctr = 1;
        self.imreader_callback = imread_safe;
    
            
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
        return (img, img_path)
        
    
    
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
    
    
    




