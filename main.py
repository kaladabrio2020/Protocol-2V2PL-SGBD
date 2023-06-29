import os
import sys
import tkinter      as tk
from   tkinter      import *
from   tkinter      import ttk
from   PIL          import Image, ImageTk
from   src.Solver   import solver

class Menu:
    def __init__(self, master):   
        self.master = master
        self.master.title('Home')
        self.master.protocol("WM_DELETE_WINDOW", self.exit)
        self.master.geometry(f'+500+280')
        self.master.resizable(True, True)

        self.frame_1 = tk.Frame(self.master)
        self.frame_2 = tk.Frame(self.master)

        ttk.Label( self.frame_1, text = 'Escrevar Schedules' ).grid(row=0, column=0)

        self.schedules = StringVar()
        ttk.Entry(
            self.frame_1, width = 40, textvariable = self.schedules
        ).grid(row=1, column=0)

        ttk.Button(
            self.frame_2, text = 'Run', command = self.Solver  
        ).grid(row=0, column=0,padx=10)
        
        ttk.Button(
            self.frame_2, text = 'Back', command = self.exit,
        ).grid(row=0, column=1)

        self.frame_1.pack(padx=10,pady=10)
        self.frame_2.pack(pady=10)
    

    def exit(self)  :sys.exit()
    def window(self):return self.master
    def Solver(self):
        solver(self.schedules.get())
        self.Popup()

    def Popup(self):
        popup = tk.Toplevel(self.master)
        popup.title('Solver')
        popup.geometry(f'+10+50')

        frame_image  = tk.Frame(popup) 
        tk.Label(frame_image,text='Imagem' ).grid(row=0,column=0)

        image   = Image.open('grafo.png')
        image   = image.resize((500,500))
        display = ImageTk.PhotoImage(image)
        
        img = tk.Label(frame_image, image=display)
        
        img.image = display
        img.grid(row=1,column=0)
        frame_image.pack()

if __name__=='__main__': ( Menu(tk.Tk()).window() ).mainloop();print(1)
