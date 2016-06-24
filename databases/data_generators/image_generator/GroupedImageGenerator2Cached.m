classdef GroupedImageGenerator2Cached

    
    properties
        cache_gig_path
        grouped_image_generator_internal
    end
    
    methods
        
        function self = GroupedImageGenerator2Cached(cached_grouped_image_generator_path,grouped_image_generator)
            self.cache_gig_path=cached_grouped_image_generator_path;
            self.grouped_image_generator_internal=grouped_image_generator;
            self.grouped_image_generator_internal.enable_caching=1;
            self.grouped_image_generator_internal.enable_pp_caching=1;
            
            
        end
        
        function self = save_cache(self)
            grouped_image_generator_internal=self.grouped_image_generator_internal;
            save(self.cache_gig_path,'grouped_image_generator_internal');
        end
        
        function self = load_cache(self)
            pull_struct=load(self.cache_gig_path,'grouped_image_generator_internal');
            self.grouped_image_generator_internal = pull_struct.grouped_image_generator_internal;
        end
        
        function self = drop_cache(self)
            self.grouped_image_generator_internal = [];
        end 
        
        
        function [self] = group_lists(self,varargin)
            self.grouped_image_generator_internal = self.grouped_image_generator_internal.group_lists(varargin);
        end
       
                
        function [self, imgs, img_paths] = next(self)
            
            [gig, imgs, img_paths] = self.grouped_image_generator_internal.reset();
            self.grouped_image_generator_internal=gig;
        end
        
        function [self, imgs, img_paths] = get(self, varargin)
            [gig, imgs, img_paths] = self.grouped_image_generator_internal.get(varargin{:});
            self.grouped_image_generator_internal=gig;
        end
        
        function [self, imgs, img_paths, pipeline_oos] = stuctured_get(self, varargin)
            [gig, imgs, img_paths, pipeline_oos] = self.grouped_image_generator_internal.stuctured_get(varargin{:});
            self.grouped_image_generator_internal=gig;
        end
        
        function self = set_image_reader(self, imreader_callback)
            self.grouped_image_generator_internal.imreader_callback = imreader_callback;
        end
        
        function [self, imgs, img_paths] = peek(self)
            [gig, imgs, img_paths] = self.grouped_image_generator_internal.get(self.ctr);
            self.grouped_image_generator_internal=gig;
        end
        
        function res = has_next(self)
            res = self.grouped_image_generator_internal.has_next();
        end
        
        
        function self = reset(self)
            self.grouped_image_generator_internal = self.grouped_image_generator_internal.reset();
        end
        
        function self = increment(self)
            self.grouped_image_generator_internal.ctr=self.grouped_image_generator_internal.ctr+1;
        end
        
        function self = set_image_modifiers(self,modification_pipelines)
            self.grouped_image_generator_internal.modification_pipelines=modification_pipelines;
        end
        
        function self = set_structured_image_modifiers(self,structured_modification_pipelines)
            self.grouped_image_generator_internal.structured_modification_pipelines=structured_modification_pipelines;
        end
        
        function out = get_func_pipeline(self)
            out=self.grouped_image_generator_internal.modification_pipelines;
        end
        
        function out = get_structured_func_pipeline(self)
            out=self.grouped_image_generator_internal.structured_modification_pipelines;
        end
        
        function dims = get_sample_dims(self, varargin)
            dims = self.grouped_image_generator_internal.get_sample_dims(varargin{:});
        end
        
        function out = get_num_samples(self)
            out=self.grouped_image_generator_internal.get_num_samples();
        end
        
        function out = get_num_groups(self)
            out = self.grouped_image_generator_internal.get_num_groups();
        end        
        
    end
    
end

