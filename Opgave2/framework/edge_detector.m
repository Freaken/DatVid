function J = edge_detector(I)

[M, N] = size(I);
J = zeros( size(I) );

Ex = [-1 -2 -1; 0 0 0; 1 2 1];
Ey = [-1 0 1; -2 0 2; -1 0 1];

for i=2:M-1
  for j=2:N-1
    
    A = I(i-1:i+1,j-1:j+1);
    val1 = sum(sum(A.*Ex));
    val2 = sum(sum(A.*Ey));
    J(i,j) = sqrt(val1^2 + val2^2);
    
  end
end

end
