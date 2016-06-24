function out = ternary_cond(cond,func1,func2,args)
    
    if(cond)
        out = func1(args{:});
    else
        out = func2(args{:});
    end

end