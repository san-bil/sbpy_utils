function new_array= interp_array(array, upsample_factor, interp_method)

if(~exist('interp_method','var'))
    interp_method='linear';
end

new_array=zeros(((size(array,1)-1)*upsample_factor+1),size(array,2));
for i=1:size(array,2)
   
    vec = array(:,i);
    interp_vec = (interp1(1:length(vec),vec,1:(1/upsample_factor):length(vec),interp_method))';
    new_array(:,i) = interp_vec; 
end