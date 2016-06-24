function [res,stdout]=system_e(cmd)

try
[res,stdout] = system(cmd,'-echo');

catch
    
end