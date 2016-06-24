function out = project_to_interval(in,lb,ub)

out = min(ub,max(lb,in));