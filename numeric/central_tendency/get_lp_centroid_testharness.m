pts = [1,2;10,9;4,1;1,12;6,8;3,6;50,1;48,2];

fighand=figure;
scatter(pts(:,1),pts(:,2));
hold all

% scatter(mean(pts(:,1)),mean(pts(:,2)))
% scatter(median(pts(:,1)),median(pts(:,2)))

%scatter(mean(pts(:,1)),mean(pts(:,2)))
%scatter(median(pts(:,1)),median(pts(:,2)))


%for i = 0.7:0.05:0.95
for i = 0.1
    new_centroid=get_lp_centroid(pts,i,fighand);
    scatter(new_centroid(1),new_centroid(2));
end

