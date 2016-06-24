function rho = admm_update_rho(rho, primal_res,dual_res,mult,diff_mult,max_rho,min_rho)

if(~exist('max_rho','var'))
    max_rho=10000;
end

if(~exist('min_rho','var'))
    min_rho=5;
end

if(sum(primal_res)>(diff_mult*dual_res))
    rho = min(rho*mult,max_rho);
elseif(sum(primal_res)<(diff_mult*dual_res))
    rho = max(rho/mult,min_rho);
else
    
end