function y = my_gmean(x,k)

n  = length(x);

xk = x.^k;
y = (sum(xk)/n)^(1/k);
