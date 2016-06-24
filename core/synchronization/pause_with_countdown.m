function pause_with_countdown(interval)

for i = 1:interval
    if(~(mod(i,2)==0))
        fprintf('%d-',i);
    end
    pause(1);
end

fprintf('done!\n');
