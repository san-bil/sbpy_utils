classdef GroupedImageGenerator

    
    properties
        file_lists
        ctr
        imreader_callback
        modification_pipelines
    end
    
    methods
        
        function self = GroupedImageGenerator(varargin)
            
            for i = 1:length(varargin)
                if(isa(varargin{i},'ImageGenerator'))
                    self.file_lists{i}=varargin{i}.file_list;
                elseif((iscell(varargin{i})))
                    self.file_lists{i}=varargin{i};
                else
                    error('You can only make a GroupedImageGenerator from cellarrays of strings or ImageGenerators.')
                end
                self.file_lists{i} = filter_empty_strings(self.file_lists{i});
            end
            self.imreader_callback = @imread;
            self.ctr = 1;
        end
        
        function [self] = group_lists(self,get_key_callback)
        
            new_file_lists=group_by(self.file_lists,get_key_callback);
            self.file_lists=new_file_lists;

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
        
        function [self, imgs, img_paths] = get(self, idx)
            
            img_paths=cell(length(self.file_lists),1);
            imgs=cell(length(self.file_lists),1);
            fprintf('GroupedImageGenerator');
            for i = 1:length(self.file_lists)
                img_path = self.file_lists{i}{idx};
                mij_path = strtrim(img_path);
                fprintf([mij_path,' ; ']);
                img = self.imreader_callback(mij_path);
                
                modified_img = apply_func_pipeline(img, self.modification_pipelines{i});
                
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
        
        function dims = get_sample_dims(self)
            
            for i = 1:length(self.file_lists)
                img_path = self.file_lists{i}{self.ctr};
                img = self.imreader_callback(strtrim(img_path));
                
                modified_img = apply_func_pipeline(img, self.modification_pipelines{i});
                
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

