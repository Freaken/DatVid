import time
import pylab
#import matplotlib.pyplot
try:
    import psyco
    psyco.full()
except:
    pass

VISUAL=True

###
#We provide a tiny climate simulation - it is only 1D!
#It is an earth-like planet with 100km atmosphere and 10 km sea
#The parameter co2 is NOT co2 content but efficiency of the greenhouse effect
#The max_sun parameter is an energy levet that, when the sun is
#at zenith will increase the temperature at the surface by max_sun degrees
###

scale=10
xsize=36*scale; ysize=11*scale; sea=10*scale; co2=90.0; max_sun=19.0
#Time to simulate
sim_days=365*100 #Simulate 100 years


#Colormaps ....
chot =   {'red':  ((0.0, 0.0, 0.0),
                   (0.96, 0.0, 0.0),
                   (0.97,0.8, 1.0),
                   (1.0, 0.8, 1.0)),

         'green': ((0.0, 0.0, 0.0),
                   (0.96, 0.0, 0.5),
                   (0.97,0.9, 0.9),
                   (1.0, 0.0, 0.0)),

         'blue':  ((0.0, 0.0, 0.4),
                   (0.96, 1.0, 0.2),
                   (0.97,0.0, 0.0),
                   (1.0, 0.0, 0.0))
        }

ctemp =   {'red':  ((0.0, 0.0, 0.0),
                   (0.96, 0.0, 0.0),
                   (0.99,0.0, 0.0),
                   (1.0, 0.0, 0.0)),

         'green': ((0.0, 0.0, 0.0),
                   (0.96, 0.0, 0.3),
                   (0.99,0.0, 0.5),
                   (1.0, 0.9, 0.9)),

         'blue':  ((0.0, 0.0, 0.4),
                   (0.96, 1.0, 1.0),
                   (0.99,1.0, 0.2),
                   (1.0, 0.0, 0.0))
        }

ccold =   {'red':  ((0.0, 0.0, 0.0),
                   (0.99,0.0, 0.0),
                   (1.0, 0.0, 0.0)),

         'green': ((0.0, 0.0, 0.0),
                   (0.99, 0.0, 0.3),
                   (1.0, 0.0, 0.5)),

         'blue':  ((0.0, 0.0, 0.4),
                   (0.99, 1.0, 1.0),
                   (1.0, 1.0, 1.0))
        }


hot = pylab.matplotlib.colors.LinearSegmentedColormap('climate_hot',chot, 256)
temp = pylab.matplotlib.colors.LinearSegmentedColormap('climate_hot',ctemp, 256)
cold = pylab.matplotlib.colors.LinearSegmentedColormap('climate_hot',ccold, 256)


###
#This is the actual simulation
#For each timestep we solve a PDE where the material constant
#decides how much energy can travel
###

def step(data, speed, up, down):
    global forward

    eps=0.1*len(data)*len(data[0])
    
    h=len(data)-1
    delta=eps+1.0
    while delta>eps:
        forward[:]=data[:]*speed+((1.0-speed)*(0.5*(up+down)))
        delta=sum(sum(abs(forward-data)))
        data[:]=forward[:]
###
#Build an ab-initio model of our world
#Not much work has been put in this function (either :))
#The important stuff is that we assign different material constant to
#water and air
###
def build_world(xsize,ysize, sea, co2):
    space_temp=-271.15
    init_temp=-100.0
    world = pylab.zeros((ysize+2,xsize))
    world += init_temp
    material = pylab.zeros((ysize+2,xsize))
    world[0]=space_temp
    j=0
    while j<sea:
        j+=1
        material[j]=(co2/100.0)
    while j<ysize-1:
        j+=1
        material[j]=0.8

    return (world, material)

#Simulate SUN
sun_angle = pylab.sin(pylab.arange(0,pylab.pi,pylab.pi/xsize))
def sun(surface_view, deg):
    surface_view+=deg*sun_angle


#Set materials for sea at .5 for ice and .75 for water
def water_ice(sea_view, sea_material):
    sea_material[:]=pylab.where(sea_view<0.0, 0.5, 0.75)

def show_gfx(world):
    if VISUAL:
        top=world.max()
        if top>50.0: cscheme=hot
        elif top>0.0: cscheme=temp
        else: cscheme=cold
        pylab.matshow(world, fignum=1, cmap=cscheme)
        pylab.draw()

#Try and read co2 level as cmd line parameter
try:
    import sys
    co2=eval(sys.argv[1])
except:
    pass
print 'CO2',co2

#Build a world based on out materials
total_world, total_material = build_world(xsize, ysize, sea, co2)
world = total_world[1:ysize+1,:]
forward=pylab.zeros(pylab.shape(world)) #A buffer used for temp data
material = total_material[1:ysize+1,:]
up = total_world[0:ysize,:]
down = total_world[2:ysize+2,:]
air_view=world[:sea-1,:]
surface_view=world[sea-1,:]
sea_view=world[sea:,:]
sea_material=material[sea:,:]


#Constants for a 24 h rotation cycle
hour_half=12*scale
hour_quart=6*scale
#A linear model of a raising/setting sun
deg_step=max_sun/hour_quart

avg=pylab.average #To keep prints shorter:)

print 'Day', 'Min' ,'Max','Surface temp', 'Air temp','Ocean temp'

#Initialize temperatures ab initio
step(world, material,up,down)
water_ice(sea_view,sea_material)
j=0
show_gfx(world)

stats=[]
print j, avg(surface_view), avg(air_view), avg(sea_view)
stats.append((avg(surface_view), avg(air_view), avg(sea_view)))
old_state=(.0,.0)
while j<=sim_days:
    j+=1
    print j, 'min',surface_view.min(),'max',surface_view.max(), sea_view.max()
    if j%365==0:
        print j, min(surface_view),'max',max(surface_view), avg(surface_view), avg(air_view), avg(sea_view)
        stats.append((avg(surface_view), avg(air_view), avg(sea_view)))
        state=(min(surface_view),'max',max(surface_view))
        if state==old_state:
            break
        old_state=state
    time_step=0
    #Simulate from sunrise to noon
    while time_step<(hour_quart):
        time_step+=1
        sun(surface_view, float(time_step)*deg_step)
        step(world, material,up,down)
        water_ice(sea_view,sea_material)
    show_gfx(world)
    #Simulate from noon to sunset
    while time_step>0:
        time_step-=1
        sun(surface_view, time_step*deg_step)
        step(world, material,up,down)
        water_ice(sea_view,sea_material)
    show_gfx(world)
    time_step=0
    #Simulate from sunset to sunrise
    while time_step<hour_half:
        time_step+=1
        step(world, material,up,down)
        water_ice(sea_view,sea_material)
    show_gfx(world)
    
#Print statistics
print 'CO2', co2, 'air temp is', avg(air_view), 'ocean temp is',avg(sea_view)
f=open('data-%s'%co2, 'w')
for i in stats:
    f.write(str(i)+'\n')
f.close()
