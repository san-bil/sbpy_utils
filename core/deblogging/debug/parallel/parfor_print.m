function parfor_print( message )

% in: a string message
%
% out: nada
%
% desc: writes the string message to the screen, with the worker ID prepended to it
%
% tags: #parfor #debugging #parallel #print #debug

t = getCurrentTask(); 
disp(['worker ' t.ID ': ' message])

end

