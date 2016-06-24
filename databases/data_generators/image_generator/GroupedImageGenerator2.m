classdef GroupedImageGenerator2

    
    properties
        file_lists
        ctr
        imreader_callback
        modification_pipelines
        structured_modification_pipelines
        enable_caching
        enable_pp_caching
        img_pp_cache
        img_pp_oo_cache
        img_cache
        opts
    end
    
    methods
        
        function self = GroupedImageGenerator2(varargin)
            
            for i = 1:length(varargin)
                if(isa(varargin{i},'ImageGenerator'))
                    self.file_lists{i}=varargin{i}.file_list;
                elseif((iscell(varargin{i})))
                    self.file_lists{i}=varargin{i};
                else
                    error('You can only make a GroupedImageGenerator2 from string-arrays or ImageGenerators.')
                end
                self.file_lists{i} = filter_empty_strings(self.file_lists{i});
            end
            self.imreader_callback = @imread_safe;
            self.ctr = 1;
            self.enable_caching=0;
            self.enable_pp_caching=0;
            self.opts={};
        end
        
        function [self] = group_lists(self,get_key_callback)
        
            new_file_lists=group_by(self.file_lists,get_key_callback);
            self.file_lists=new_file_lists;

        end
        
        function [out] = dynamic_func(self,key,varargin)
            
            fhandle = kv_get(key,self.opts);
            out = fhandle(varargin{:});
            
        end

                
        function [predicate_masks, joint_pred_mask] = get_predicate_masks(self,predicate_list)
            
            
            file_list_size=length(self.file_lists{1});
            num_predicates=length(predicate_list);
            predicate_masks=repmat({zeros(file_list_size,predicate_list)},3,1);

            for i =1:length(self.file_lists)
                file_list=self.file_lists{i};
                for j = 1:length(file_list)
                    for k = 1:num_predicates
                        handle=predicate_list{k};
                        predicate_masks{i}(j,k) = handle(file_list{j});
                    end
                end
            end
            
            joint_pred_mask=ones(file_list_size,predicate_list);
            for i =1:length(predicate_masks)
                joint_pred_mask = joint_pred_mask & predicate_masks{i};
            end

            
        end

        
        
        
        function res = has_next(self)
            res=self.ctr<length(self.file_lists{1});
        end

        
        function self = reset(self)
            self.ctr=1;
        end
                
        function [self, imgs, img_paths] = next(self)
            
            [self, imgs, img_paths] = self.peek();
            self = self.increment();
            
        end
        
        function [self, imgs, img_paths] = get(self, idx, pipeline_mask, invert_pipeline_mask)
            if(~exist('pipeline_mask','var'));pipeline_mask={};end;
            if(~exist('invert_pipeline_mask','var'));invert_pipeline_mask=1;end;
            
            img_paths=cell(length(self.file_lists),1);
            imgs=cell(length(self.file_lists),1);
            fprintf('GroupedImageGenerator2');
            for i = 1:length(self.file_lists)
                
                img_path = self.file_lists{i}{idx};
                mij_path = strtrim(img_path);

                if(self.enable_caching && kv_haskey(mij_path,self.img_cache))
                    img = kv_get(mij_path,self.img_cache);
                    fprintf([mij_path,'(using cache) ; ']);
                elseif(self.enable_caching && ~kv_haskey(mij_path,self.img_cache))
                    img = self.imreader_callback(mij_path);
                    self.img_cache = kv_set(mij_path,img,self.img_cache);
                    fprintf([mij_path,'(caching) ; ']);
                else
                    img = self.imreader_callback(mij_path);
                    fprintf([mij_path,' ; ']);
                end
               
                pp_cache_key=sanitize_string([mij_path str(pipeline_mask) str(invert_pipeline_mask)]);
                if(self.enable_pp_caching && kv_haskey(pp_cache_key,self.img_pp_cache))
                    modified_img = kv_get(pp_cache_key,self.img_pp_cache);
                    fprintf([mij_path,'(using img_pp_cache) ; ']);
                elseif(self.enable_pp_caching && ~kv_haskey(pp_cache_key,self.img_pp_cache))
                    modified_img = apply_func_pipeline_masked(img, self.modification_pipelines{i}, pipeline_mask, invert_pipeline_mask);
                    self.img_pp_cache = kv_set(pp_cache_key,modified_img,self.img_pp_cache);
                    fprintf([mij_path,'(caching to img_pp_cache) ; ']);
                else
                    modified_img = apply_func_pipeline_masked(img, self.modification_pipelines{i}, pipeline_mask, invert_pipeline_mask);
                    fprintf([mij_path,' ; ']);
                end
                
                
                imgs{i} = modified_img;
                img_paths{i} = img_path;
            end
            fprintf('\n');
        end
        
        function [self, imgs, img_paths, pipeline_oos] = stuctured_get(self, idx, pipeline_mask, invert_pipeline_mask)
            global v_tracker_for_block_consistency
            if(~exist('pipeline_mask','var'));pipeline_mask={};end;
            if(~exist('invert_pipeline_mask','var'));invert_pipeline_mask=1;end;
            
            img_paths=cell(length(self.file_lists),1);
            imgs=cell(length(self.file_lists),1);
            pipeline_oos=cell(length(self.file_lists),1);
            fprintf('GroupedImageGenerator');
            for i = 1:length(self.file_lists)
                img_path = self.file_lists{i}{idx};
                mij_path = strtrim(img_path);
                v_tracker_for_block_consistency=i;
                if(self.enable_caching && kv_haskey(mij_path,self.img_cache))
                    img = kv_get(mij_path,self.img_cache);
                    fprintf([mij_path,'(using cache) ; ']);
                elseif(self.enable_caching && ~kv_haskey(mij_path,self.img_cache))
                    img = self.imreader_callback(mij_path);
                    self.img_cache = kv_set(mij_path,img,self.img_cache);
                    fprintf([mij_path,'(caching) ; ']);
                else
                    img = self.imreader_callback(mij_path);
                    fprintf([mij_path,' ; ']);
                end
                
                
                pipeline_mask_str=kv_get(double(isempty(pipeline_mask)),kv_create_w_names((1),'emptypipelinemask',(0),str(pipeline_mask)));
                pp_cache_key=sanitize_string(path_join(mij_path, pipeline_mask_str, ['ipm_' str(invert_pipeline_mask)]));
                if(self.enable_pp_caching && kv_haskey(pp_cache_key,self.img_pp_cache))
                    modified_img = kv_get(pp_cache_key,self.img_pp_cache);
                    oo = kv_get(pp_cache_key,self.img_pp_oo_cache);
                    fprintf([mij_path,'(using img_pp_cache) ; ']);
                elseif(self.enable_pp_caching && ~kv_haskey(pp_cache_key,self.img_pp_cache))
                    [modified_img, oo] = apply_func_pipeline_masked_wrapped(img, self.structured_modification_pipelines{i}, pipeline_mask, invert_pipeline_mask);
                    self.img_pp_cache = kv_set(pp_cache_key,modified_img,self.img_pp_cache);
                    self.img_pp_oo_cache = kv_set(pp_cache_key,oo,self.img_pp_oo_cache);
                    fprintf([mij_path,'(caching to img_pp_cache) ; ']);
                else
                    [modified_img, oo] = apply_func_pipeline_masked_wrapped(img, self.structured_modification_pipelines{i}, pipeline_mask, invert_pipeline_mask);
                    fprintf([mij_path,' ; ']);
                end

                
                pipeline_oos{i} = oo;
                imgs{i} = modified_img;
                img_paths{i} = img_path;
            end
            fprintf('\n');
        end
        
        function self = set_image_reader(self, imreader_callback)
            self.imreader_callback = imreader_callback;
        end
        
        function [self, imgs, img_paths] = peek(self)
            
            [self, imgs, img_paths] = self.get(self.ctr);
            
        end
        
        function self = increment(self)
            self.ctr=self.ctr+1;
        end
        
        function self = set_image_modifiers(self,modification_pipelines)
            self.modification_pipelines=modification_pipelines;
        end
        
        function self = set_structured_image_modifiers(self,structured_modification_pipelines)
            self.structured_modification_pipelines=structured_modification_pipelines;
        end
        
        function out = get_func_pipeline(self)
            out=self.modification_pipelines;
        end
        
        function out = get_structured_func_pipeline(self)
            out=self.structured_modification_pipelines;
        end
        
        function dims = get_sample_dims(self, pipeline_mask, invert_pipeline_mask)
            
            if(~exist('pipeline_mask','var'));pipeline_mask={};end;
            if(~exist('invert_pipeline_mask','var'));invert_pipeline_mask=1;end;
            
            for i = 1:length(self.file_lists)
                img_path = self.file_lists{i}{self.ctr};
                img = self.imreader_callback(strtrim(img_path));
                
                modified_img = apply_func_pipeline_masked(img, self.modification_pipelines{i}, pipeline_mask, invert_pipeline_mask);
                
                imgs{i} = modified_img;
            end
            dims = cellfun(@size,imgs,'UniformOutput',0);
                
        end
        
        function out = get_num_samples(self)
            out = length(self.file_lists{1});
        end
        
        function out = get_num_groups(self)
            out = length(self.file_lists);
        end
        
    end
    
end

