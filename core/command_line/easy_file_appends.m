function easy_file_appends(dict)

keys = kv_getkeys(dict);

for i =1:length(keys)

    path = keys{i};
    text = kv_get(keys,dict);

    easy_file_appends(text,path)
end