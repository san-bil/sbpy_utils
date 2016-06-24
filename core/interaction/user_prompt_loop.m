function out = user_prompt_loop(initial_prompt, input_filters_w_failure_responses)


while(1)

    user_input = input(initial_prompt,'s');
    
    input_filters = input_filters_w_failure_responses(:,1);
    failure_responses = input_filters_w_failure_responses(:,2);

    filter_res = cellfun(@(tmp)tmp(user_input),input_filters);
    
    
    if(all(filter_res))
        out = user_input;
        break;
    else
        failure_responses_filtered=failure_responses(~filter_res);
        cellfun_uo0(@(tmp)disp_out(tmp),failure_responses_filtered);
    end
end