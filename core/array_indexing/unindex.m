function out=unindex(vals, idxs, to_unindex)

out = to_unindex;
out(idxs)=vals;