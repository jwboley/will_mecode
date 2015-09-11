from mecode import G

import numpy as np

#Thanks Alex!!

com_press = 16 #Mega com port for pressure (Make sure you verify!)
pressure = 0.5
vps_high = 10 #High speed velocity to move to initial print location
vps = 0.5 #Operating print speed
h0_high = 2 #Nozzle offset for high speed motion to initial print location
h0 = 0.1 #Operating nozzle offset
pdwell = 1 #Dwell time for fluid despensing at start of print job

g = G(
      direct_write = False,
      outfile = r'/Users/jwboley/Documents/will_mecode/Variable_Meander.pgm',
      header = r'/Users/jwboley/Documents/will_mecode/mymegacasterheader.txt',
      footer = r'/Users/jwboley/Documents/will_mecode/mymegacasterfooter.txt',
      print_lines = False,
      )
      
#Remember to zero at lower left corner via 'G92 X0 Y0 Z0'

margin = 2
xl = 2*2.54*10-2*margin #2" by 3" slide
yl = 3*2.54*10-2*margin #2" by 3" slide
x0 = margin
y0 = 2*margin+yl
 
n = 4 #number of lines for each spacing

g.set_pressure(com_press, pressure)
g.feed(vps_high)
g.abs_move(z = h0_high)
g.abs_move(x = x0, y = y0)
g.feed(vps)
g.abs_move(z = h0)
g.toggle_pressure(com_press)
g.dwell(pdwell)
    
def s_meander(n,xl,p):
    for i in range(n):
        if i%2 == 0:
            c = 'CW'
            sense = 1
        else:
            c = 'CCW'
            sense = -1
            
        g.move(x = sense*(xl-p/2))
        g.arc(x = 0, y = -p, radius = p/2, direction = c)

s_meander(n = n, xl = xl, p = 1.0)#calls meander function
g.view(backend = 'matplotlib')#plot print path
g.teardown()#ends the script (never comment out)