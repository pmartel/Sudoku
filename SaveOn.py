""" make a simple note taking program that will save on close """

from tkinter import *

class SaveOn():
    tk = None
    filename = None
    closing = False
    closeEv = []
    
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
        #self.top.bind('<Destroy>',self.__SaveOnClosing)
        self.top.protocol("WM_DELETE_WINDOW", self.__SaveOnClosing)
        #print(self.txt.bindtags())
        pass

    # menu command handlers
    def __openHandler(self):
        self.checkChanged()
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
        check = self.checkChanged()
        if check == 'ok':
            print('Opening new file');
            self.filename = None
            self.txt.edit_modified(False)
        else:
            print( 'Old data unchanged')
        pass

    def __saveHandler(self):
        if self.filename == None:
            self.__saveAsHandler()
            return
        print('Saving',self.filename)
        self.txt.edit_modified(False)
        pass
    
    def __saveAsHandler(self):
        oldFileName = self.filename
        self.filename = filedialog.asksaveasfilename(defaultextension='.txt',
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

    def __SaveOnClosing(self):
        if not self.closing:
            ret = self.checkChanged()
            print('checkchanged returned',ret)
            if ret != 'cancel':
                print('closing Save on')
                self.top.destroy()
                pass
            #self.closing = True
        pass

    def checkChanged(self):
        """ ask the usere if s/he wants to save if the text is changed """
        if self.txt.edit_modified():
            self.msg = messagebox.askyesnocancel('Save Data?',
                                              'Text is not saved.  Save it?')
            if self.msg == None:
                return 'cancel'
            elif self.msg:
                self.__saveHandler()
            return 'ok'

######################################################################
# Main program
######################################################################
        
s= SaveOn()
