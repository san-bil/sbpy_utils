function rsyncs(inputs, dst, rsync_args, varargin)

for i = 1:length(inputs)

    src = inputs{i};
    rsync(src, dst, rsync_args, varargin{:})
        
end


