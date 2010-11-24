import Control.Applicative

g = 1 -- Gravitational constant scaled to 1
s = 1 -- Time-step size scaled to 1 

data Planet = Planet { pos :: [Double], vel :: [Double], mass :: Double } deriving(Eq, Show)

vplus = zipWith (+)
vminus = zipWith (-)
vmult s = map (*s)

step ps p = Planet new_pos new_vel (mass p)
    where others = filter (/=p) ps
          diff_vectors = vminus (pos p) . pos <$> others
          dists = sqrt . sum . map (^2) <$> diff_vectors
          new_vel = foldl vplus (vel p) $ zipWith3 (\r p -> vmult (-(mass p)*g/r^3)) dists others diff_vectors
          new_pos = pos p `vplus` (map (*s) new_vel)

all_step ps = map (step ps) ps

simulation ps = print ps >> simulation (all_step ps)
main = simulation [Planet [1,0] [0,0] 0.001, Planet [0,1] [0,-0.1] 0.005]
