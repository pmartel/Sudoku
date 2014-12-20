""" This file is a one cell of a sudoku game."""
from tkinter import *

class Cell:
    row = []
    col = []
    box = []
    val = ''
    origVal = ''
    oldchar = ''
    
    def __init__(self, r, c, box, can, game):
        
        self.row = r
        self.col = c
        self.box = box
        self.tk = can
        self.game = game # to reference things at the game level
        self.size=game.nSq
        
        if self.size == 16:
            self.base = 16
        else:
            self.base = 10
        # set up Entry widget
        siz = game.boxSize
        xo = game.xOff
        yo = game.yOff
        
        sv = StringVar()
        okCmd = can.register(self.isOk)
        self.ent = Entry(can,justify=CENTER, width=1,font=('Arial',16),\
                    textvariable=sv, validate='all',\
                    validatecommand=(okCmd,'%P','%s','%V') )
        self.w = can.create_window(c*siz+2*xo,r*siz+2*yo,anchor = NW,\
                              height = siz-2*xo, width=siz-2*yo,window=self.ent)


    def isOk(self, c, oldC, reason):
        dic = self.game.digits[self.size]
        e = self.ent # the Entry
        # debug data
        s = 'row {0} col {1} new<{2}> old<{3}> {4}'.format(\
            self.row,self.col,c,oldC, reason)
        print(s)
        if len(c) > 2:
            print( 'c is too long')
        elif len(c) == 2:
            

        return c in dic
        return True
    
    def reset(self):
        self.val = self.origVal

    def getv(self):
        return self.ent.get()

    def setv(self,v):  # note: just set() overloads the builtin class set
##        if self.val == ' ':
##            self.val.set(str(v))
##        else:
##            # some warning if you try to load over a non-blank?
##            pass
##for n in range(81):
##    e = entList[n]
##    v=e['text'] # has the form PY_VARn
##    e.setvar(v,str(n+1))
##        self.val.set(str(v))
##also
##e.select_range(0,1)
        pass
        
    def pressed(self):
        v = input('? ')
        vInt = int(v,self.base)
        if vInt >= 1 and vInt <= self.size :
            self.setv(vInt)
        else:
            print('Bad value. Should be digit between 1 and',self.size)
        pass
