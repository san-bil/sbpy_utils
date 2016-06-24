function disp_cellstr(string_arr, str_prefix, use_stderr)

if(~exist('str_prefix','var'));str_prefix='';end;
if(~exist('use_stderr','var'));use_stderr=0;end;

for i = 1:length(string_arr)
   if(~use_stderr)
        fprintf('%s%s\n',str_prefix,string_arr{i});
   else
       fprintf(2, '%s%s\n',str_prefix,string_arr{i});
   end
end