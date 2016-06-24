function arr = assignat(arr, idx, val)
  if(isnumeric(arr))
    arr(idx) = val;
  else
    arr{idx} = val;
  end
end