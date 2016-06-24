function copy_files(inputs, dst, unix_impl, excludes)

for i = 1:length(inputs)
    if(exist('unix_impl','var') && unix_impl==1)
        args_string = build_string_args(excludes);
        cmd_str = ['rsync -avuzh ' args_string inputs{i} ' ' dst];
        disp(cmd_str);
        [out1,out2] = system(cmd_str);
    else
        copyfile(inputs{i},dst);
    end
end

end

