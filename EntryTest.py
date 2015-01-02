""" Test code for learning about entry widgets """

from tkinter import *

class EntryTest(Frame):
    #parameters
    boxSize = 50
    xOff = 3
    yOff = 3

    def __init__(self, tk):

        # set up the graphics
        self.tk = tk
        tk.title('Entry widget test')
        tk.geometry('500x500')
        super(EntryTest,self).__init__(tk)
        self.top = self.winfo_toplevel()

        # set up the Entries
        self.eList=[]
        for r in range(2):
            for c in range(2):
                sv = StringVar()
                okCmd = self.top.register(self.isOk)
                en =Entry(self.top, justify=CENTER, font=('Arial',16),
                          textvariable=sv,
                          validate='key',
                          validatecommand=(okCmd,'%d','%i','%P','%s','%S',
                                     '%v','%V','%W')
                          )
                en.grid(row=r,column=c)
                self.eList.append( en )
                
        pass
    
    """ Callback substitution codes:
        '%d' - Action code: 0 for an attempted deletion, 1 for an attempted insertion, or -1 if the callback was
    called for focus in, focus out, or a change to the textvariable.
        '%i' - When the user attempts to insert or delete text, this argument will be the index of the beginning
    of the insertion or deletion. If the callback was due to focus in, focus out, or a change to the
    textvariable, the argument will be -1.
        '%P' - The value that the text will have if the change is allowed.
        '%s' - The text in the entry before the change.
        '%S' - If the call was due to an insertion or deletion, this argument will be the text being inserted or
    deleted.
        '%v' - The current value of the widget's validate option
        '%V' - The reason for this callback: one of 'focusin', 'focusout', 'key', or 'forced' if the
    textvariable was changed
        '%W' - The name of the widget.

    Use them all for now, print them for debug
        
    """
    def isOk(self, d, i, p, s, S, v, V, W):
        retVal = False
##        debug data
        print( 'isOk called with:')
        print( 'self',self)
        print( '  %d',d)
        print( '  %i',i)
        print( '  %p',p)
        print( '  %s',s)
        print( '  %S',S)
        print( '  %v',v)
        print( '  %V',V)
        print( '  %W',W)

        # we want only one character, so
        if V == 'key':
            #self.setv(S)
            e = self.whoAmI(W)
            var = e['textvariable']
            e.setvar(var,S)
            e['validate']='key'
            pass
        return False

    """ dump info about Entry[n] """
    def dump(self,n):
        e = self.eList[n]
        print( 'Info for entry',n);
        keys = e.keys()
        for k in keys:
            print(k,':',e[k])
        pass
    
    """ take the 'name' of an Entry under this class and return the Entry """
    def whoAmI( self, name ):
        for e in self.eList:
            if e._w == name:
                return e
            pass
        return None
    
# main routine
# This creates a window
root = Tk()

# start the T\test
et = EntryTest(root)
#et.mainloop()
# for debug
l = et.eList


    

    
