function out = folder_contains_filetype(folder,filetype)

matching_files = unix_find(folder, ['.' filetype],{}, 1,{'-print','-quit'});

out = ~isempty(matching_files);