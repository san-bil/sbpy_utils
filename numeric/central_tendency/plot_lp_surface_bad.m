function plot_lp_surface_bad(X,p)

figure;

xrange=-10:0.5:60;
yrange=-10:0.5:20;

obj_surface=zeros(round(numel(yrange))*round(numel(xrange)),1);
ctr=1;


for i=xrange
    for j=yrange

    candidate = [i,j];
    objective_val=nd_sum(abs(X-repmat(candidate,[size(X,1),1])).^(p)).^(1/p);
    
    obj_surface(ctr)=objective_val;
    ctr=ctr+1;
    end
end

obj_surface_reshaped= unflatten_image( obj_surface,numel(xrange),numel(yrange));
surf(yrange,xrange,obj_surface_reshaped);