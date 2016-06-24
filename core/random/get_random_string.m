function randString = get_random_string(sLength)


s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

%find number of random characters to choose from
numRands = length(s); 

%generate random string
randString = s( max(1,round(rand(1,sLength)*numRands)) );
