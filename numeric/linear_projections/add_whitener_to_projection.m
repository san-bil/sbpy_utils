function [M, Xwh] = add_whitener_to_projection(M, X, tol)

if(~exist('tol','var'))
    tol=0.0000001;
end

[Xwh,~,~,whitenerX] = whiten((M*X)', tol);
M = whitenerX'*M;
