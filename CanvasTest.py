# test of using Canvas with buttons
from tkinter import *
from time import *

test = Tk()
test.title( "Canvas Test")
siz = 50
xo=3
yo=xo
gs='{0}x{1}'.format(siz*10,siz*10)
test.geometry(gs)
n=3
n2 = n*n

can = Canvas(test,height=n2*siz+yo, width=n2*50+xo, bg='light gray')
can.grid(row=1,column=1)

winList =[]
entList=[]
hLin = []
vLin = []
#draw outline
for x in range(0,n2+1):
    if x % 3 == 0:
        wid = 3
    else:
        wid = 1
    hLin.append(can.create_line(0,x*siz+yo,500,x*siz+yo,fill='black',width=wid))
    vLin.append(can.create_line(x*siz+xo,0,x*siz+xo,500,fill='black',width=wid))

for r in range(n2):
    for c in range(n2):
        sv = StringVar()
        ent = Entry(can,justify=CENTER, width=1,font=('Arial',16),\
                    textvariable=sv)
        entList.append(ent)
        w = can.create_window(c*siz+2*xo,r*siz+2*yo,anchor = NW,\
                              height = siz-2*xo, width=siz-2*yo,window=ent)
        winList.append(w)

        
#can.bell()
#t = Toplevel(height=100,width=100)

for n in range(81):
    e = entList[n]
    v=e['text']
    e.setvar(v,str(n+1))


