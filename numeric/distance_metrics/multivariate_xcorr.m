function crosscor_matrix = multivariate_xcorr(X,Y)

% in: two observation matrices of equal length, with columns representing identical variables, but from different signal sources
%
% out: a 2D cross-correlation matrix, where entry (i,j) is the cross-correlation of X(:,i) with Y(:,j).
%
% desc: As above. Input matrices are standardised to have zero mean and unit variance
%
% tags: #crosscorrelation

num_samples = size(X,1);

X = X-repmat(mean(X,1),num_samples,1);
Y = Y-repmat(mean(Y,1),num_samples,1);

crosscov_matrix = (X'*Y)/num_samples;

x_std = std(X,1);
y_std = std(Y,1);

normalizing_variance_matrix = x_std'*y_std;

crosscor_matrix = crosscov_matrix ./ normalizing_variance_matrix;
