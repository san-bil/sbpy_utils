function [tmp]=apply_func_pipeline(input, func_pipeline) 

tmp = input;
for k = 1:length(func_pipeline)    
    func_h = func_pipeline{k};
    tmp=func_h(tmp);
end
    
    