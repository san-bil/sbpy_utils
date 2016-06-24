function out = get_cctv_frame_idx(filename)

out = (strrep(index_cellarray(strsplit(strip_extension(basename(filename)),'_'),1),'frame',''));