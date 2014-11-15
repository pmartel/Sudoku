# test of using Canvas with buttons
from tkinter import *

test = Tk()
test.title( "Canvas Test")
test.geometry('500x500')
can = Canvas(test,height=300, width=300, bg='green')
can.grid(row=1,column=1)
n = 0
hLin = []
vLin = []
for x in range(1,6):
    hLin.append(can.create_line(0,x*50,500,x*50,fill='blue'))
    vLin.append(can.create_line(x*50,0,x*50,500,fill='red'))

can.bell()
