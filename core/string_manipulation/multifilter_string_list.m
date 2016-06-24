function clean_list = multifilter_string_list(list,regex_list,exclusive)

if(~exist('exclusive','var'))
    exclusive=0;
end

clean_list = list;
for i = 1:length(regex_list)

    clean_list = filter_string_list(clean_list,regex_list{i},exclusive);

end
