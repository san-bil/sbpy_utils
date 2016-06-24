function [ simple_time ] = get_simple_time()

% in: nada
%
% out: time string formatted as e.g. '20h30m'
%
% desc: (as above)
%
% tags: #time #datetime

mydate = clock;
h = mydate(4);
m = mydate(5);
simple_time = strcat(num2str(h),'h',num2str(m),'m');

end

