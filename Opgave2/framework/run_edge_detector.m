clear all;
close all;

RGB = imread('lena_part.jpg');
I = double( rgb2gray(RGB) );
J = edge_detector(I);

figure(1);
clf;
imagesc( I );
hold on;
axis tight;
colorbar;
colormap gray;
title('Input Image');
hold off;

figure(2);
clf;
imagesc( J );
hold on;
axis tight;
colorbar;
colormap gray;
title('Edge Image');
hold off;
print('-f2', '-dpng' ,'my_edges');
