from mecode import G
import numpy as np

g = G(
      direct_write = False,
      ### When Editing On Megacaster ###
      #outfile = r'\\seasfs02.rc.fas.harvard.edu\jlewis_lab\User Files\Boley\Print_Routines\Variable_Speed_Meander.pgm',
      #header = r'C:\Users\Aerosol Jet\Documents\GitHub\will_mecode\mymegacasterheader.txt',
      #footer = r'C:\Users\Aerosol Jet\Documents\GitHub\will_mecode\mymegacasterfooter.txt',
      ### When Editing On Laptop ###
      #outfile = r'/Users/jwboley/Documents/will_mecode/Variable_Speed_Meander.pgm',
      #header = r'/Users/jwboley/Documents/will_mecode/mymegacasterheader.txt',
      #footer = r'/Users/jwboley/Documents/will_mecode/mymegacasterfooter.txt',
      ### When Editing On Minicaster ###
      outfile =r'C:\Users\User\Documents\GitHub\will_mecode\Variable_Speed_Meander.pgm',
      header=None,
      footer=r'C:\Users\User\Documents\GitHub\will_mecode\casterfooter.txt',
      aerotech_include=False,
      print_lines=False,
      )
      
#Remember to zero at lower left corner via 'G92 X0 Y0 Z0'
#Move printhead to desired starting location (X,Y, and Z) before printing

margin = 0 #set up margins from edge of slide
xl = 2*2.54*10 #2" by 3" slide
xl = 30
yl = 3*2.54*10 #2" by 3" slide


#####glass slide border used for print path troubleshooting######
#g.move(x=2*2.54*10) 
#g.move(y=3*2.54*10)
#g.move(x=-2*2.54*10)
#g.move(y=-3*2.54*10)
#################################################################
  
      
n = 4 #number of lines for each unit meander  
def unit_meander(n,xl,p,v,ctr,q):
    g.feed(v)
    i = 0
    while i < n:
        if (ctr*n+i)%2 == 0:
            c = 'CCW'
            g.abs_move(x = 2*xl - margin)
            g.arc(x = 0, y = p, radius = p/2, direction = c)
        else:
            c = 'CW'
            g.abs_move(x = xl + margin)
            g.arc(x = 0, y = p, radius = p/2, direction = c)
        i += 1
        
p = 3.5 #pitch between meanders in mm
N = 4 #total number of unit meanders
d = 0.2 #inner diameter of nozzle in mm
v0 = 0.9 #speed for first unit meander in mm/s
vN = 1.8 #speed for Nth unit meander in mm/s
alpha = np.power((vN/v0),1.0/(N-1))
tl = 0.25 #maximum allowable print time for the slowest trace in minutes
xl = min([xl,tl*60*v0])

def meta_meander(xl,N,n,p0,v0,alpha,d):
    j = 0
    while j < N:
        v = v0*np.power(alpha,j)
        q = np.pi/4*v*np.power(d*np.power(10,-3),2)#flow rate in m^3/s
        g.dwell(1)
        unit_meander(n=n,xl=xl,p=p0,v=v,ctr=j,q=q)
        j += 1

meta_meander(xl=xl,N=N,n=n,p0=p,v0=v0,alpha=alpha,d=d)
g.feed(vN)
g.abs_move(x = 2*xl+5.0) 
g.view(backend = 'matplotlib')#plot print path
g.teardown()#ends the script (never comment out)