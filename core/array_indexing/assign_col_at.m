function arr = assign_col_at(arr, idx, val)
if(nargin==0)
    fprintf('\n\t\tUsage: assign_col_at(array, idx, val)\n\n');
    return;
end

  if(isnumeric(arr))
    arr(:,idx) = val;
  else
    arr{:,idx} = val;
  end
end