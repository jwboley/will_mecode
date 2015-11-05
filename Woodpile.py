from mecode import G

import numpy as np

#Thanks Alex!!

g = G(
      direct_write = False,
      outfile = r'\\seasfs02.rc.fas.harvard.edu\jlewis_lab\User Files\Boley\Print_Routines\Woodpile.pgm',
      header = r'C:\Users\Aerosol Jet\Documents\GitHub\will_mecode\mymegacasterheader.txt',
      footer = r'C:\Users\Aerosol Jet\Documents\GitHub\will_mecode\mymegacasterfooter.txt',
      print_lines = False,
      aerotech_include=False,
      )
      
#Remember to zero at lower left corner via 'G92 X0 Y0 Z0'

defspeed = 7 
d = 410.0/np.power(10,4) #nozzle diameter (cm)
q = np.pi/4*np.power(d,2)*defspeed/10 #flow rate (cm/s)
filthickness=0.61 # mm

layeroffset=0.8*filthickness

widthoffset =1.5

xlen=10

ylen=10

zlen=2

numxpasses=int(np.ceil(xlen/(2*widthoffset)))
numypasses=int(np.ceil(ylen/(2*widthoffset)))
numlayers=int(np.ceil(zlen/layeroffset))
overshoot=1.5*filthickness
truexlen=2*overshoot+(2*numxpasses-1)*widthoffset
trueylen=2*overshoot+(2*numypasses-1)*widthoffset
g.feed(defspeed)
g.move(y=-5)

for nz in range(0,numlayers):

    if nz%4==0:

        xdir=1

        ydir=-1

    elif nz%4==1:

        xdir=-1

        ydir=-1

    elif nz%4==2:

        xdir=-1

        ydir=1

    else:

        xdir=1

        ydir=1

    if ((nz%4==0) or (nz%4==2)):

        for nx in range(0,numxpasses):

            g.move(y=ydir*trueylen)

            g.move(x=xdir*widthoffset)

            g.move(y=-ydir*trueylen)

            if nx<(numxpasses-1):

                g.move(x=xdir*widthoffset)

            else:

                g.move(x=xdir*overshoot,y=ydir*overshoot)

    else:

        for ny in range(0,numypasses):

            g.move(x=xdir*truexlen)

            g.move(y=ydir*widthoffset)

            g.move(x=-xdir*truexlen)

            if ny<(numypasses-1):

                g.move(y=ydir*widthoffset)

            else:

                g.move(x=xdir*overshoot,y=ydir*overshoot)

    g.move(z=layeroffset)



g.move(y=17)

g.move(z=-layeroffset*numlayers)

g.view(backend='matplotlib')

g.teardown()