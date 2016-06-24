function msg = log_call(varargin)

stack_frame=dbstack(1);

if(nargin==0)
    msg = [class(varargin{1}) ': ' stack_frame.name '(...)'];
else
    msg = [stack_frame.name '(...)'];
end

