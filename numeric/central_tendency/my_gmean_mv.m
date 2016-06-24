function Y = my_gmean_mv(X,k)

Y = zeros(1,size(X,2));
for i =1:size(X,2)
    x=X(:,i);
    n  = length(x);
    xk = x.^k;
    y = (sum(xk)/n)^(1/k);
    Y(i)=y;
end