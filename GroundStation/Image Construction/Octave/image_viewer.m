clc
clear

B = zeros(240,320);
C = zeros(320,320);
count = 0;
split = 1;

[A] = dlmread( 'log1.txt', ',');
disp(length(A));

#for m = 1:240
#  C(1:300 ,m) = [A(m, 1:end) A(m+1, 1:end) A(m+2, 1:end)];
#endfor
q = zeros(7,100);

A = [A;q];

s = reshape(A',100*4,240)';



for i = 1:240
    for j = 1:320
        count = count + 1;
        #if count < length(A)  
        B(j,i) = A(count);
        #endif
    endfor
endfor

image(s,'CDataMapping','scaled');
colorbar;