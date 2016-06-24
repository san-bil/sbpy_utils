function windowed_xcorr_tensor = get_windowed_multivariate_xcorr(sample_matrix_1, sample_matrix_2, sequence_column)

% in: observation matrix 1;
%     observation matrix 2;
%     monotonic integer vector denoting sequence membership e.g. [1 1 1 1 1 2 2 2 3 3 4 4 5 5 5 6]
%
%
% out: a 3-tensor with as many z-slices as sequences, where each z-slice is the 2D cross-correlation matrix
%      of the corresponding sequence
%
% desc: (as above)
%
% tags: #sequences #crosscorrelation #tensor 
%
% TODO: rename - this is not windowed!

sequence_ids = my_unique(sequence_column);
num_sequences = length(sequence_ids);

windowed_xcorr_tensor = zeros(size(sample_matrix_1,2),size(sample_matrix_2,2),num_sequences);



for i = 1:num_sequences
    try 
        sequence_id = sequence_ids(i);
        
        sequence_1_data = sample_matrix_1(sequence_column==sequence_id,:);
        sequence_2_data = sample_matrix_2(sequence_column==sequence_id,:);
        
        window_xcorr = multivariate_xcorr(sequence_1_data,sequence_2_data);
        windowed_xcorr_tensor(:,:,i) = window_xcorr;
        
    catch err
        disp(err)
    end
end



end
