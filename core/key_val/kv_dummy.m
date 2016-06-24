function kvm = kv_dummy(kv_length)

kvm = {};
for i = 1:kv_length
   
    
    kvm{i,1}=get_random_string(3);
    kvm{i,2}=get_random_string(5);
    
end