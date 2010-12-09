function [] = run_edge_detector(imgin, imgout)
RGB = imread(imgin);
I = double( rgb2gray(RGB) );
J = edge_detector(I);
J = J ./ max(max(J));
imwrite(J, imgout, 'png');
