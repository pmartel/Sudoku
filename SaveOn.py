""" make a simple note taking program that will save on close """

from tkinter import *

class SaveOn():
    tk = None
    filename = None
    changed = False

    def __init__(self):
        tk = Tk()
        self.tk = tk
        self.f = Frame(self.tk)
        tk.title('SaveOn notes - Phil Martel')
        tk.geometry('500x500')
        #super(SudokuGame,self).__init__(tk)
        txt = Text(tk)
        self.txt = txt
        txt.grid(column=0,row=0)
        #add menu
        self.top = self.tk.winfo_toplevel()
        self.menuBar = Menu(self.top)
        self.top['menu'] = self.menuBar
        #File
        self.subMenuFile = Menu(self.menuBar)
        self.menuBar.add_cascade(label='File', menu=self.subMenuFile,
                                 underline=0)
        self.subMenuFile.add_command(label='New', command=self.__newHandler,
                                     underline=0)
        self.subMenuFile.add_command(label='Open', command=self.__openHandler,
                                     underline=0)
        self.subMenuFile.add_command(label='Save',underline=0,
                                     command=self.__saveHandler)
        self.subMenuFile.add_command(label='Save As',underline=5,
                                     command=self.__saveAsHandler)
        self.subMenuFile.add_command(label='Print',underline=0,
                                     command=self.__PrintHandler)
            
        # setting up to interrupt destroy
        self.top.bind('<Destroy>',self.__SaveOnClosing)
        print(self.txt.bindtags())
        pass

    # menu command handlers
    def __openHandler(self):
        oldFileName = self.filename
        self.filename = filedialog.askopenfilename(
            filetypes=[('Text Files','.txt'), ('All Files', '.*')])
        if self.filename == '':
            self.filename = oldFileName
            print('File open cancelled')
        else:
            print('Opening',self.filename);
            self.changed = False
        pass

    def __newHandler(self):
        if self.changed:
            print('file changed.  Save?')
        print('Opening new file');
        self.filename = None
        pass

    def __saveHandler(self):
        if self.filename == None:
            self.__saveAsHandler()
            return
        print('Saving',self.filename)
        pass
    
    def __saveAsHandler(self):
        oldFileName = self.filename
        self.filename = filedialog.asksaveasfilename(defaultextension='.sud',
            filetypes=[('Text Files','.txt'), ('All Files', '.*')])
        if self.filename == '':
            self.filename = oldFileName
            print('File Save As cancelled')
        else:
            self.__saveHandler()
        pass

    def __PrintHandler(self):
        print('printing',self.filename)
        pass

    def __SaveOnClosing(self, ev):
        print('closing Save on,  Event',ev)
        
s= SaveOn()
