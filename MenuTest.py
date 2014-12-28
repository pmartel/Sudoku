""" This file is me learning about menus """

from tkinter import *
#messagebox is a module in tkinter which has multiple classes
# importing from it lets you avoid messagebix.showinfo(), but it may cause
# clashes
#from tkinter.messagebox import *
from tkinter import filedialog

class MenuTest(Frame):
    gString = '300x300'
    
    def __init__(self, tk, n=3):
        """ tk is the tkinter object that will display the window. """
        # set up the graphics
        self.tk = tk
        tk.title('Menu Test - Phil Martel')
        tk.geometry(self.gString)
        super(MenuTest,self).__init__(tk)

        # add a menu
        self.top = self.winfo_toplevel()
        self.menuBar = Menu(self.top)
        self.top['menu'] = self.menuBar
        #File
        self.subMenuFile = Menu(self.menuBar)
        self.menuBar.add_cascade(label='File', menu=self.subMenuFile)
        self.subMenuFile.add_command(label='Open', command=self.__openHandler)
        #Help
        self.subMenuHelp = Menu(self.menuBar)
        self.menuBar.add_cascade(label='Help', menu=self.subMenuHelp)
        self.subMenuHelp.add_command(label='About', command=self.__aboutHandler)
        pass

    def __aboutHandler(self):
        self.help = messagebox.showinfo( title='Playing with the GUI',
                 message='Menu Test')
        pass

    def __openHandler(self):
        self.fd = filedialog.FileDialog(self)
##        self.file=self.fd.Open()
        pass
# main routine
# This creates a window
root = Tk()

# start the game
m = MenuTest(root)
#m.mainloop()
# for debug
