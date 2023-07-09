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
        string = solver(self.schedules.get())
        self.Popup(string)

    def Popup(self,string):
        popup = tk.Toplevel(self.master)
        popup.title('Solver')
        popup.geometry(f'+10+50')

        frame_gera   = tk.Frame(popup)
        frame_image  = tk.Frame(frame_gera)
        frame_texto  = tk.Frame(frame_gera) 
        tk.Label(frame_image,text='Grafo de serialização' ).grid(row=0,column=0)

        image   = Image.open('grafo.png')
        image   = image.resize((420,450))
        display = ImageTk.PhotoImage(image)
        
        img = tk.Label(frame_image, image=display)
        
        img.image = display
        img.grid(row=1,column=0)

        tk.Label(frame_texto,text='Passos' ).grid(row=0,column=0)

        texto = tk.Text(frame_texto, height = 25,width = 40)
        texto.insert(END, string)
        
        texto.grid(row=1,column=0)

        frame_texto.grid(row=0,column=1,padx=5,pady=5)
        frame_image.grid(row=0,column=0,padx=5,pady=5)
        frame_gera.pack()

if __name__=='__main__': 
    solver('r1(tp1)w1(tp1)r2(a1)w2(a1)c2c1')
    # ( Menu(tk.Tk()).window() ).mainloop()
