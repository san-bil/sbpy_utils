function kv_unpack(dict,varargin)

for i = 1:size(dict,1)

    key = dict{i,1};
    val = dict{i,2};
    
    if(~isempty(varargin))
        if(ismember(key,varargin))
            assignin('caller', key, val);
        end
    else 
        assignin('caller', key, val);
    end
end
