pts = [1 2 2.5 4 6 9.5 10 10.1 45 46 47]';

scatter(pts,ones(size(pts)));
hold all

scatter(mean(pts),1)
scatter(median(pts),1)


for i = 0.8:0.05:0.95
    new_centroid=get_lp_centroid(pts,i);
    scatter((5),new_centroid(1));
end

