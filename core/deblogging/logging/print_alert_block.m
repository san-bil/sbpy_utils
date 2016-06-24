function print_alert_block(msg,character,block_height)

tabbing = 6;
if(exist('msg','var'))
    block_width=project_to_interval(length(msg)+tabbing,15,50);
else
    block_width=20;
end

if(~exist('block_height','var')),block_height=3;end;
if(~exist('character','var')),character='@';end;


for i =1:ceil(block_height/2)
    disp(repmat(character,1,block_width));
end
disp('')
if(exist('msg','var')),disp([repmat(' ',1,tabbing) msg]);end;
disp('')
for i =1:ceil(block_height/2)
    disp(repmat(character,1,block_width));
end
