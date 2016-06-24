function print_log_message(required_loglevel,loglevel,basestr,varargin)

if(loglevel>=required_loglevel)
    fprintf(basestr,varargin{:});
end