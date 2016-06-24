function [centroid] = get_lp_centroid(X,p,fighand)

if(~exist('fighand','var'))
    fighand=figure;
end
% if(numel(p)==1)
%     p=repmat(p,1,size(X,2));
% end
%assert(all(p<=1))

x_centroid = median(X,1);
x_centroid_av = x_centroid;
%x_centroid=rand(1,size(X,2));
t=1;
full_grad = zeros(size(x_centroid));

step_size=1;
hold all;
while(1)
   step_size=1/(1+t);
   step_size=0.999*step_size;

   full_grad_old=full_grad;
   x_centroid_old = x_centroid;
   x_centroid_av_old=x_centroid_av;

   grad_callback = @(tmp)p.*(abs(tmp-x_centroid).^(p-1)).*sign(tmp-x_centroid);
   grads = fast_rowfun(X, grad_callback);
   full_grad = sum(grads,1);
   full_grad_norm=norm(full_grad);
   
   smoothed_full_grad=(((t-1)/t)*full_grad_old)+((1/t)*full_grad);
   step_norm=norm(step_size*smoothed_full_grad);
   x_centroid = (x_centroid)+(step_size*smoothed_full_grad);
   x_centroid_av = (((t-1)/t)*x_centroid_old)+((1/t)*x_centroid);
   objective=nd_sum(abs(X-repmat(x_centroid,[size(X,1),1])).^(p))^(1/p);
  
   print_var(full_grad_norm); print_var(full_grad); print_var(smoothed_full_grad);print_var(objective);print_var(step_norm);

   if(abs(x_centroid_av-x_centroid_av_old)<0.000001),print_var(t),break;end
   
   t=t+1;
   x_centroid_cell=my_mat2cell(x_centroid_av);
   if(size(x_centroid_cell)==1),x_centroid_cell{2}=1;end
   scatter(x_centroid_cell{:},'filled');
   pause(0.005);
end
tmp=1;
close(fighand);

centroid = x_centroid;