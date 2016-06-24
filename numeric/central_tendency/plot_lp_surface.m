function plot_lp_surface(X,p)

figure;

xrange=max(X(:,1))-min(X(:,1));
yrange=max(X(:,2))-min(X(:,2));

obj_surface=zeros(round(yrange),round(xrange));

for i=min(X(:,1)):max(X(:,1))
    for j=min(X(:,2)):max(X(:,2))

    candidate = [j,i];
    objective_val=nd_sum(abs(X-repmat(candidate,[size(X,1),1])).^(p))^(1/p);
    obj_surface(j,i)=objective_val;
    end
end


imagesc(obj_surface);