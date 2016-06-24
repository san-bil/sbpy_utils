function S = combination2(s)

%COMBINATION - returns all combinations of a set s (two fold combinations)
%
% AUTHOR:   M.F. Valstar
% CREATED:  25102005
%
%IN:  s: set to create combinations from
%OUT: S: set of twofold combinations

S = [];
while ~isempty(s)
    r = setdiff(s, s(1));
    while ~isempty(r)
        S = vertcat(S,[s(1), r(1)]);
        r = setdiff(r, r(1));
    end
    s = setdiff(s, s(1));
end