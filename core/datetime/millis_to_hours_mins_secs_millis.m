function time_string = millis_to_hours_mins_secs_millis(milliseconds,delim)

% in: a duration in milliseconds
%
% out: a time-string formatted as e.g. '2:10:30:500'
%
% desc: (as above)
%
% tags: #millis #timeconversion #datetime #time #timing #duration

if(~exist('delim','var'))
    delim=':';
end

hours = floor(milliseconds/3600000);
rem_after_hours = mod(milliseconds,3600000);

minutes = floor(rem_after_hours/60000);
rem_after_minutes = mod(rem_after_hours,60000);

seconds = floor(rem_after_minutes/1000);
rem_after_seconds = mod(rem_after_hours,1000);

time_string = sprintf('%s%s%s%s%s%s%s',...
                        num2str_mod(hours,2),...
                        delim,...
                        num2str_mod(minutes,2),...
                        delim,...
                        num2str_mod(seconds,2),...
                        delim,...
                        num2str_mod(rem_after_seconds,3)...
                        );

end
