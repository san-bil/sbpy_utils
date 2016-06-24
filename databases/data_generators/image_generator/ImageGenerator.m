classdef ImageGenerator

    
    properties
        file_list
        ctr
        modification_pipeline
        imreader_callback
    end
    
    methods
        
        function self = ImageGenerator(file_list)
            self.file_list=file_list;
            self.ctr = 1;
            self.imreader_callback = @imread;
        end
        
        function self = reset(self)
            self.ctr=1;
        end
        
        function self = increment(self)
            self.ctr=self.ctr+1;
        end
        
        function self = set_image_modifiers(self,modification_pipeline)
            self.modification_pipeline=modification_pipeline;
        end
        
        function dims = get_sample_dims(self)
            
            img_path = self.file_list{1};
            img = self.imreader_callback(strtrim(img_path));

            modified_img = apply_func_pipeline(img, self.modification_pipeline);
                
            dims = size(modified_img);
                
        end
        
        function [self, img, img_path] = get(self, idx)
            
            img_path = self.file_list{idx};
            img_path = strtrim(img_path);
            fprintf([img_path,' ; ' newline]);
            raw_img = self.imreader_callback(img_path);
            img = apply_func_pipeline(raw_img, self.modification_pipeline);
            
        end
        
        function [self, img, img_path] = next(self)
            
            [self, img, img_path] = self.peek();
            self = self.increment();
        end
        
        function out = get_num_samples(self)
            out = length(self.file_list);
        end
        
        function [self, img, img_path] = peek(self)
            
            [self, img, img_path] = self.get(self.ctr);
            
        end
        
        function self = set_image_reader(self, imreader_callback)
            self.imreader_callback = imreader_callback;
        end
        
        function res = has_next(self)
            res=self.ctr<length(self.file_list);
        end
        
        
    end
    
end

