""" This file handles the menu for SudokuGame.py """
from tkinter import *

class SudokuMenu(Frame):
    def __init__( self,parent ):
        self.parent = parent
        self.top = parent.winfo_toplevel()
        self.menuBar = Menu(self.top)
        self.top['menu'] = self.menuBar
        #File
        self.subMenuFile = Menu(self.menuBar)
        self.menuBar.add_cascade(label='File', menu=self.subMenuFile)
        self.subMenuFile.add_command(label='New', command=self.__newHandler)
        self.subMenuFile.add_command(label='Open', command=self.__openHandler)
        self.subMenuFile.add_command(label='SaveAs',
                                     command=self.__saveAsHandler)
        self.subMenuFile.add_command(label='Print',
                                     command=self.__PrintHandler)
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
        self.filename = filedialog.askopenfilename(
            filetypes=[('Sudoku Files','.sud'), ('All Files', '.*')])
        self.parent.load(self.filename)
        pass

    def __newHandler(self):
        self.parent.clear()
        pass

    def __saveAsHandler(self):
        self.filename = filedialog.asksaveasfilename(defaultextension='.sud',
            filetypes=[('Sudoku Files','.sud'), ('All Files', '.*')])
        self.parent.save(self.filename)
        pass

    def __PrintHandler(self):
        self.parent.print()
        pass
