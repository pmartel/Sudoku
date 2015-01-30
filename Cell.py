""" This file is a one cell of a sudoku game."""
from tkinter import *

class Cell:
    row = []
    col = []
    box = []
    options = [] # list of possible digits if val == ' '
    digits = [] # list of legitmate digits for isOk()
    val = ''
    origVal = ''
    oldchar = ''
    idx = -1
    
    def __init__(self, r, c, box, can, game):
        
        self.row = r
        self.col = c
        self.box = box
        self.idx = r * game.nDigits + c
        self.tk = can
        self.game = game # to reference things at the game level
        self.size=game.nDigits
        
        if self.size == 16:
            self.base = 16
        else:
            self.base = 10
        self.digits = self.game.digits[self.size]

        # set up Entry widget
        siz = game.boxSize
        xo = game.xOff
        yo = game.yOff
        
        sv = StringVar()
        top = game.winfo_toplevel()
        okCmd = top.register(self.isOk)
        self.ent = Entry(can, justify=CENTER, width=1, font=('Arial',16),
                    textvariable=sv, validate='focusin',
                    validatecommand=(okCmd,'%d','%i','%P','%s','%S',
                                     '%v','%V','%W') )
        self.w = can.create_window(c*siz+2*xo,r*siz+2*yo,anchor = NW,
                                   height = siz-2*xo, width=siz-2*yo,
                                   window=self.ent)
        self.setv(' ')

    """ Callback substitution codes:
        '%d' - Action code: 0 for an attempted deletion, 1 for an attempted insertion, or -1 if the callback was
    called for focus in, focus out, or a change to the textvariable.
        '%i' - When the user attempts to insert or delete text, this argument will be the index of the beginning
    of the insertion or deletion. If the callback was due to focus in, focus out, or a change to the
    textvariable, the argument will be -1.
        '%P' - The value that the text will have if the change is allowed.
        '%s' - The text in the entry before the change.
        '%S' - If the call was due to an insertion or deletion, this argument
    will be the text being inserted or deleted.
        '%v' - The current value of the widget's validate option
        '%V' - The reason for this callback: one of 'focusin', 'focusout',
    'key', or 'forced' if the textvariable was changed
        '%W' - The name of the widget.

    Use them all for now, print them for debug
        
    """
    def isOk(self, d, i, P, s, S, v, V, W):
        ''' This checks if the key entered is legitimate ''' 
        retVal = False
        # debug data
##        print( 'isOk called with:')
##        print( 'self',self)
##        print( '  %d',d)
##        print( '  %i',i)
##        print( '  %P<{0}>'.format(P))
##        print( '  %s<{0}>'.format(s))
##        print( '  %S<{0}>'.format(S))
##        print( '  %v',v)
##        print( '  %V',V)
##        print( '  %W',W)
##        print( 'entry[',self.idx,'] validate',self.ent['validate'])

        #print('Cell',self.idx,'has focus')
        self.game.focusIdx = self.idx
        if V == 'key':
            if len(S)>1:
                print('S is too long')
            else:
                if S in self.digits:
                    # S is a good new value, save the old value, jam new one in
                    self.setvStack(S)
         #whether the new value is good or bad, don't let it be changed
        # by the routine that called us.
        return False
    
    def reset(self):
        self.val = self.origVal

    def getv(self):
        return self.ent.get()

    def setv(self,v):  # note: just set() overloads the builtin class "set"
##        print("in setv for cell[{0}] set '{1}'".format(self.idx,v))
        if v in self.digits:
            e = self.ent # the Entry
            nam = e['text'] # the name of the StringVar
            e.setvar(nam,v)
            e['validate']='key'
            return True
        return False
    
    def setvStack(self, v):
        old = self.getv()
        self.game.undoStack.append((self.idx, old))
        self.setv(v)
        
    def check(self):
        """ verify that the value of this cell is legal """
        retval = True
        v = self.getv()
        if v == ' ' or v == '':
            #a blank cell is OK
            return True
        for n in range(self.size):
            cel = self.game.cell[n]
            if cel == self : # self is ok
                continue
            cv = cel.getv()
            if cv != v :
                continue
            #Same value. Check row, column and box
            if self.row == cel.row:
                return False
            elif self.col == cel.col:
                return False
            elif self.box == cel.box:
                return False
            pass
        return True


        
