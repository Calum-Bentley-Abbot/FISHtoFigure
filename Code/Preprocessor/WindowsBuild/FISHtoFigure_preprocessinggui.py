# -*- coding: utf-8 -*-
"""
GUI for preprocessing script for FISHtoFigure

"""

import tkinter as tk

import FISHtoFigure_preprocessingmain as F2Fpre

class dataconcat():
    def __init__(self, master):   
        self.master = master
        master.title("FISHtoFigure preprocessor")
        master.geometry('1270x200')
        self.frame = tk.Frame(self.master)
        self.frame.grid_rowconfigure(1, minsize = 40)
        self.frame.grid_rowconfigure(5, minsize = 20)
            
        self.main_header = tk.Label(self.frame, text = 'Welcome to the FISHtoFigure preprocessor', font='Helvetica 9 bold')
        self.main_header.grid(row = 0, columnspan = 3)
        
        self.analysis_header = tk.Label(self.frame, text = 'Provide path to data directory containing datasets for concatenation:', font='Helvetica 9 bold')
        self.analysis_header.grid(row = 1, column = 0)
            
        self.in_label = tk.Label(self.frame, text = 'Enter Input Folder path:')
        self.in_label.grid(row = 3, column = 0)
            
        self.folder = tk.Entry(self.frame, width = 50, borderwidth = 5)
        self.folder.grid(row = 3, column = 1)
            
        self.folder_button = tk.Button(self.frame, text = 'Find', width = 25, command = self.file_locator, bg = '#71C0A7')
        self.folder_button.grid(row = 4, column = 3)
        
        self.run_button = tk.Button(self.frame, text = 'Run', width = 25, borderwidth = 5, command = self.run, bg = '#71C0A7')
        self.run_button.grid(row = 6, column = 3)
        
        self.frame.pack()
        
    def file_locator(self):
        location = self.folder.get()
        out = tk.Label(self.frame, text = f'Folder selected:   ...{location[-30:]}')
        out.grid(row = 3, column = 3)
        self.input_folder = repr(location.strip('"') +"\\").strip("'")
        print(f'Input folder: {self.input_folder}')
        

    def run(self):
        self.master.destroy()

root = tk.Tk()
preprocessor = dataconcat(root)
root.mainloop()


#Runs FISHtoFigure preprocessing
F2Fpre.run(preprocessor.input_folder)
