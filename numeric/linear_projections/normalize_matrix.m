function out = normalize_matrix(in, thresh)

%thresh in this case is 1/(mu1*eta1)

[U,sigma,V] = svd(in,'econ');
sigma = diag(sigma);
svp = length(find(sigma > thresh));

if svp >= 1
    sigma = ones(svp,1);
else
    svp = 1;
    sigma = 0;
end

out = U(:,1:svp)*diag(sigma)*V(:,1:svp)';