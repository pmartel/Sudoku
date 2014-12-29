""" This file handles the menu for SudokuGame.py """
from tkinter import *

class SudokuMenu(Frame):
    def __init__( self,master ):
        self.top = master.winfo_toplevel()
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
        self.help = messagebox.showinfo( title='Sudoku',
                 message='Sudoku Game by Phil Martel 2014')
        pass

    def __openHandler(self):
        #this opens some kind of box, but how to use it?
        #self.fd = filedialog.FileDialog(self)
        #self.file=self.fd.Open()
        self.file = filedialog.askopenfilename()
        pass
