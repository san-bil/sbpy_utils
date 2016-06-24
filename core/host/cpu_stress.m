function cpu_stress(x)

% in: number of cores on cpu
%
% out: nada
%
% desc: causes max cpu-utilization on x cores of CPU
%
% tags: #stresstest #multithreading #workers #workerpool #parfor

if(~exist('x','var'))
    x=1
end

fprintf('Ctrl+C to stop stress test...\n')
matlabpool('open',x);

try
    parfor i = 1:1000
        j = 1;
        while(1)

            x = rand(128,128);
            y = inv(x);
            if(mod(j,100000)==0)
                fprintf('%s\n',int2str(j));
                !top | grep -m 1 Cpu
            end
        end
    end
catch err
    fprintf('Stopped stress test...\n')
    matlabpool('close');
end
