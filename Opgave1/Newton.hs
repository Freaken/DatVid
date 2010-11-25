import Control.Applicative

g = 1 -- Gravitational constant scaled to 1
s = 1 -- Time-step size scaled to 1 

data Planet = Planet { pos :: [Double], vel :: [Double], mass :: Double } deriving(Eq, Show)

vplus = zipWith (+)
vminus = zipWith (-)
vmult s = map (*s)

step ps p = Planet npos nvel (mass p)
    where others = filter (/=p) ps
          diffs = map (`vminus` pos p) $ map pos others
          dists = sqrt . sum . map (^2) <$> diffs
          nvel = foldl vplus (vel p) . map (vmult s) $
            zipWith3 (\r k -> vmult (mass k*g/r^3)) dists others diffs
          npos = pos p `vplus` (s `vmult` nvel)

all_step ps = map (step ps) ps

simulation ps = print ps >> simulation (all_step ps)
main = simulation [Planet [0] [0] 0.001, Planet [1] [0] 0.005]
