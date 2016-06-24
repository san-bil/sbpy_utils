function out=callerfunc(upsteps)

if(~exist('upsteps','var'))
    upsteps = 3;
end
mystack=dbstack;
out = mystack(upsteps).name;