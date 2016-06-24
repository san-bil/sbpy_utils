function arr = assign_row_at(arr, idx, val)
  if(isnumeric(arr))
    arr(idx,:) = val;
  else
    arr{idx,:} = val;
  end
end