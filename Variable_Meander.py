from mecode import G

import numpy as np

#Thanks Alex!!

com_press = 16 #Mega com port for pressure (Make sure you verify!)
pressure = 40
vps_high = 10 #High speed velocity to move to initial print location
vps = 5 #Operating print speed
h0_high = 2 #Nozzle offset for high speed motion to initial print location
h0 = 0.6 #Operating nozzle offset
pdwell = 1 #Dwell time for fluid despensing at start of print job

g = G(
      direct_write = False,
      outfile = r'\\seasfs02.rc.fas.harvard.edu\jlewis_lab\User Files\Boley\Print_Routines\Variable_Meander.pgm',
      header = r'C:\Users\Aerosol Jet\Documents\GitHub\will_mecode\mymegacasterheader.txt',
      footer = r'C:\Users\Aerosol Jet\Documents\GitHub\will_mecode\mymegacasterfooter.txt',
      print_lines = False,
      aerotech_include=False,
      )
      
#Remember to zero at lower left corner via 'G92 X0 Y0 Z0'

margin = 8
xl = 2*2.54*10 #2" by 3" slide
yl = 3*2.54*10 #2" by 3" slide



x0 = margin
y0 = 2*margin+yl
# 

#####glass slide border used for print path troubleshooting######
#g.move(x=2*2.54*10) 
#g.move(y=3*2.54*10)
#g.move(x=-2*2.54*10)
#g.move(y=-3*2.54*10)
#################################################################

g.set_pressure(com_press, pressure)
g.feed(vps_high)
g.abs_move(z = h0_high)
g.abs_move(x = x0, y = yl-margin)
g.feed(vps)
g.abs_move(z = h0)
g.toggle_pressure(com_press)
g.dwell(pdwell)
  
  
n = 4 #number of lines for each unit meander  
def unit_meander(n,xl,p):
    for i in range(n):
        if i%2 == 0:
            c = 'CW'
            g.abs_move(x = xl - margin)
            g.arc(x = 0, y = -p, radius = p/2, direction = c)
        else:
            c = 'CCW'
            g.abs_move(x = margin)
            g.arc(x = 0, y = -p, radius = p/2, direction = c)


p0 = 7.8 #pitch for first unit meander
pN = 0.2 #pitch for Nth unit meander
r = ((yl-margin)-n*p0)/((yl-margin)-n*pN) #factor reduction for spacing of subsequent meanders
N = int(np.rint(np.log(pN/p0)/np.log(r))) #total number of unit meanders
p0 = pN/np.power(r,N) #redefine p0 to account for rounding error

def meta_meander(xl,n,N,r,p0):
    for i in range(N):
        pi = p0*np.power(r,i)
        unit_meander(n=n,xl=xl,p=pi)
        

g.toggle_pressure(com_press)
g.feed(10)
g.clip(height=2, direction='-x')


meta_meander(xl=xl,n=n,N=N,r=r,p0=p0) 
g.view(backend = 'matplotlib')#plot print path
g.teardown()#ends the script (never comment out)