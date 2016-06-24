function [A,B,r,U,V] = full_cca(X,Y)
%CANONCORR Canonical correlation analysis.
%   [A,B] = CANONCORR(X,Y) computes the sample canonical coefficients for
%   the N-by-P1 and N-by-P2 data matrices X and Y.  X and Y must have the
%   same number of observations (rows) but can have different numbers of
%   variables (cols).  A and B are P1-by-D and P2-by-D matrices, where D =
%   min(rank(X),rank(Y)).  The jth columns of A and B contain the canonical
%   coefficients, i.e. the linear combination of variables making up the
%   jth canonical variable for X and Y, respectively.  Columns of A and B
%   are scaled to make COV(U) and COV(V) (see below) the identity matrix.
%   If X or Y are less than full rank, CANONCORR gives a warning and
%   returns zeros in the rows of A or B corresponding to dependent columns
%   of X or Y.
%
%   [A,B,R] = CANONCORR(X,Y) returns the 1-by-D vector R containing the
%   sample canonical correlations.  The jth element of R is the correlation
%   between the jth columns of U and V (see below).
%
%   [A,B,R,U,V] = CANONCORR(X,Y) returns the canonical variables, also
%   known as scores, in the N-by-D matrices U and V.  U and V are computed
%   as
%
%      U = (X - repmat(mean(X),N,1))*A and
%      V = (Y - repmat(mean(Y),N,1))*B.


if nargin < 2
    error(message('stats:canoncorr:TooFewInputs'));
end

[n,p1] = size(X);
if size(Y,1) ~= n
    error(message('stats:canoncorr:InputSizeMismatch'));
elseif n == 1
    error(message('stats:canoncorr:NotEnoughData'));
end
p2 = size(Y,2);

% Center the variables
X = X - repmat(mean(X,1), n, 1);
Y = Y - repmat(mean(Y,1), n, 1);

% Factor the inputs, and find a full rank set of columns if necessary
% [Q1,T11,perm1] = qr(X,0);
% rankX = sum(abs(diag(T11)) > eps(abs(T11(1)))*max(n,p1));
% if rankX == 0
%     error(message('stats:canoncorr:BadData', 'X'));
% elseif rankX < p1
%     warning(message('stats:canoncorr:NotFullRank', 'X'));
%     Q1 = Q1(:,1:rankX); T11 = T11(1:rankX,1:rankX);
% end
% [Q2,T22,perm2] = qr(Y,0);
% rankY = sum(abs(diag(T22)) > eps(abs(T22(1)))*max(n,p2));
% if rankY == 0
%     error(message('stats:canoncorr:BadData', 'Y'));
% elseif rankY < p2
%     warning(message('stats:canoncorr:NotFullRank', 'Y'));
%     Q2 = Q2(:,1:rankY); T22 = T22(1:rankY,1:rankY);
% end

[Q1,T11,perm1] = qr(X,0);
[Q2,T22,perm2] = qr(Y,0);

% Compute canonical coefficients and canonical correlations.  For rankX >
% rankY, the economy-size version ignores the extra columns in L and rows
% in D. For rankX < rankY, need to ignore extra columns in M and D
% explicitly. Normalize A and B to give U and V unit variance.

% d = min(rankX,rankY);
% [L,D,M] = svd(Q1' * Q2,0);
% A = T11 \ L(:,1:d) * sqrt(n-1);
% B = T22 \ M(:,1:d) * sqrt(n-1);
% r = min(max(diag(D(:,1:d))', 0), 1); % remove roundoff errs
% 
% % Put coefficients back to their full size and their correct order
% A(perm1,:) = [A; zeros(p1-rankX,d)];
% B(perm2,:) = [B; zeros(p2-rankY,d)];

[L,D,M] = svd(Q1' * Q2,0);
A = T11 \ L(:,:) * sqrt(n-1);
B = T22 \ M(:,:) * sqrt(n-1);
r = min(max(diag(D(:,:))', 0), 1); % remove roundoff errs

% Put coefficients back to their full size and their correct order
A(perm1,:) = A;
B(perm2,:) = B;

% Compute the canonical variates
if nargout > 3
    U = X * A;
    V = Y * B;
end