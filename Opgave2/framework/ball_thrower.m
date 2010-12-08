clear all;
close all;

m = 1;
g = 9.81;
dt = 0.01;

x0 = 0;
y0 = 1;
vx0 = 2;
vy0 = 2;

[X Y] = ball_simulate( x0, y0, vx0, vy0, dt, m, g  );

figure(1);
clf;
plot(X,Y,'-xr');
hold on;
xlabel('distance [M]');
ylabel('height [M]');
title('Ball Throw Result');
hold off;
