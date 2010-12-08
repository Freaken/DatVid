function [X Y] = ball_simulate(x0, y0, vx0, vy0, dt, m, g)

x  = x0;
y  = y0;
vx = vx0;
vy = vy0;

X  = [];
Y  = [];

while y>0
  
  [x y vx vy] = ball_step(x,y,vx,vy,dt,m,g);
  
  X = [X x];
  Y = [Y y];
end

end