function [ map ] = kv_read( file )

fid = fopen(file);
allData = textscan(fid,'%s','Delimiter','\n');
fclose(fid);
strings = allData{1};
map = cell(length(allData),2);
for i =1:length(strings)
   
    map(i,:) = strsplit(allData{1}{i},'=');
    
end



