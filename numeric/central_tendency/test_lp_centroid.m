function [out,seq] = test_lp_centroid(X,centroid,p)

(X-repmat(centroid,size(X,1)).^p)

while(1)
   old_x_centroid = x_centroid;
   seq = [seq;old_x_centroid];
   grad_callback = @(tmp)p.*(abs(tmp-x_centroid).^(p-1)).*sign(tmp-x_centroid);
   grads = fast_rowfun(X, grad_callback);
   full_grad = sum(grads,1);
   x_centroid = x_centroid-full_grad();
   if(abs(x_centroid-old_x_centroid)<0.000001)
       print_var(get_lp_centroid_ctr)
       break;
   end
end

out = x_centroid;