function [ dirs ] = list_dirs( parent_dir )

dirs={};

contents = dir(parent_dir);

for i = 3:length(contents)
    tmp_name = [parent_dir filesep contents(i).name];
    if(exist(tmp_name,'dir')==7)
        dirs = [dirs;tmp_name];
    end
end


end

