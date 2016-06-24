function [ simple_date ] = get_simple_date()

% in: nada
%
% out: date-time string formatted as e.g. '2014-1-1_13_37'
%
% desc: (as above)
%
% tags: #date #time #datetime

my_date = clock;
year = num2str(my_date(1));
month  = num2str(my_date(2));
day  = num2str(my_date(3));
hour  = num2str(my_date(4));
minute  = num2str(my_date(5));
second = num2str(my_date(6));

simple_date = [year,'-',month,'-',day,'_',hour,'h',minute,'m'];

end

