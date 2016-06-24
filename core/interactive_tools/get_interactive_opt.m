function choice = get_interactive_opt(choices, prompt="INTERACTIVE - ", callback)

if(~exist('prompt','var')),prompt='INTERACTIVE - ';end
if(~exist('callback','var')),callback=@(tmp)tmp;end

choices_str=concat_cell_string_array(choices,', ',1);
choice=user_prompt_loop([prompt ' (' choices_str ') : ' ], ...
                               {@(tmp)ismember(tmp,choices), ['Please enter one of: ',choices_str]});
choice=callback(choice);
