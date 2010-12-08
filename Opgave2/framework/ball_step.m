function [x, y, vx, vy] = ball_step(x, y, vx, vy, dt, m, g)

x = x + dt*vx;
y = y + dt*vy;
vy = vy - dt*g;

end
