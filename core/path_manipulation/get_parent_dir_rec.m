function curr = get_parent_dir_rec( file_path, height )

curr=file_path;
for i=1:height
    curr = get_parent_dir(curr);
end

end