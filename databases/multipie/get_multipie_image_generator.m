function generator = get_multipie_image_generator(opts)

if(ischar(opts) && strcmp(opts,'help'))
    disp('options are: session (int in {1...4}), subject , expression , camera (frontal, {far,mid}x{left,right}) ')
    generator=[];
else

    matcher = get_multipie_file_path(opts);
    root_folder = '/vol/hci2/Databases/video/MultiPIE';

    if(~exist(root_folder,'dir')==7)
        error('    You need to mount the multipie database at /vol/hci2/Databases/video/MultiPIE   ')
    end

    generator = get_image_generator(root_folder,matcher,1);
end
