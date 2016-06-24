function out = grouped_image_generator_getbatch(image_generator, batch_idxs)

disp('Loading image batch...')
num_groups = image_generator.get_num_groups();
num_samples = image_generator.get_num_samples();
dim = image_generator.get_sample_dims();
real_dim  =dim{1}(1);

if(ischar(batch_idxs) && strcmp(batch_idxs,'all'))
    batch_idxs = 1:num_samples;   
end

batch_num_samples = length(batch_idxs);
assert(batch_num_samples>0)

group_arrays = repmat({zeros(real_dim,batch_num_samples)},num_groups,1);

for i = 1:length(batch_idxs)
    
    if(mod(i,100)==0)
        disp(['Loaded ' num2str(i)]);
    end
        
    real_idx = batch_idxs(i);
    [~, imgs, ~] = image_generator.get(real_idx);
    
    for j = 1:num_groups
        group_arrays{j}(:,i) = imgs{j};
    end

end

out = group_arrays;
