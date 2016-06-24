function clipped_idx = clip_array_index(idx, lower, upper)

    clipped_idx = max(lower, min(upper,idx));

end
