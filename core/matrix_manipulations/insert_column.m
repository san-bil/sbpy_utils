function [ modified_dataset ] = insert_column( column, dataset, position )

% in: column vector, numeric matrix, column index
%
% out: numeric matrix with column vector inserted at given column index
%
%                  ( [3]    [1 2 4]        )                   [1 2 3 4]
%  insert_column   ( [3]  , [1 2 4]  ,  3  )    would give     [1 2 3 4]
%                  ( [3]    [1 2 4]        )                   [1 2 3 4]
%
%
% desc: as above.
%
% tags: #dataset #insertion #column


modified_dataset = [dataset(:,1:position-1) column dataset(:,position:end)];

end

