# -*- coding: utf-8 -*-
"""
FISHtoFigure GUI, allows for input folder selection by path, the selection of analysis options
and the specification of flags and dataset names for plotting
"""

import tkinter as tk
from tkinter import ttk as ttk


import FISHtoFigure_main as F2F


class usrin():
    def __init__(self, master):   
        self.master = master
        master.title("FISHtoFigure")
        master.geometry('1380x620')
        self.frame = tk.Frame(self.master)
        self.frame.grid_rowconfigure(1, minsize = 40)
        self.frame.grid_rowconfigure(5, minsize = 20)
        self.frame.grid_rowconfigure(15, minsize = 60)
        self.frame.grid_rowconfigure(18, minsize = 40)
        self.frame.grid_rowconfigure(22, minsize = 50)
        self.frame.grid_columnconfigure(4, minsize = 160)
        self.frame.grid_columnconfigure(7, minsize = 320)
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.main_header = tk.Label(self.frame, text = 'Welcome to FISHtoFigure, please provide path to data location, analysis preferences, and make sure to seperate names in channel and dataset lists with a comma and single space', font='Helvetica 9 bold')
        self.main_header.grid(row = 0, columnspan = 7)
        
        self.analysis_header = tk.Label(self.frame, text = 'Provide path to input data directory:', font='Helvetica 9 bold')
        self.analysis_header.grid(row = 1, column = 0)
        
        
        self.in_label = tk.Label(self.frame, text = 'Enter Input Folder path:')
        self.in_label.grid(row = 3, column = 0)
            
        self.folder = ttk.Entry(self.frame, width = 30)
        self.folder.grid(row = 3, column = 1)
            
        self.folder_button = tk.Button(self.frame, text = 'Find', width = 25, command = self.file_locator, bg = '#71C0A7')
        self.folder_button.grid(row = 4, column = 7)
        
        
        self.box_header = tk.Label(self.frame, text = 'Select analysis options:', font='Helvetica 9 bold')
        self.box_header.grid(row = 6, column = 0)
            
        self.var_hist = tk.IntVar()
        self.check_hist = tk.Checkbutton(self.frame, text = 'Plot transcript occurances', variable = self.var_hist)
        self.check_hist.grid(row = 7, column = 0)
 
        self.var_scatter = tk.IntVar()
        self.check_scatter = tk.Checkbutton(self.frame, text = 'Plot transcript distribution', variable = self.var_scatter)
        self.check_scatter.grid(row = 10, column = 0)
        
        self.threshold_label = tk.Label(self.frame, text = 'Positive cell threshold:')
        self.threshold_label.grid(row = 10, column = 4)
        
        self.threshold = ttk.Entry(self.frame, width = 15)
        self.threshold.grid(row = 10, column = 5)
        
        self.var_expression = tk.IntVar()
        self.check_expression = tk.Checkbutton(self.frame, text = 'Transcript abundance analysis', variable = self.var_expression)
        self.check_expression.grid(row = 11, column = 0)
        
        
        
        
        self.var_dubposA = tk.IntVar()
        self.check_dubposA = tk.Checkbutton(self.frame, text = 'Multi-target transcript abundance', variable = self.var_dubposA)
        self.check_dubposA.grid(row = 12, column = 0)
        
        self.dubposA_chans_label = tk.Label(self.frame, text = 'First set of multi-positive channels:')
        self.dubposA_chans_label.grid(row = 12, column = 1)
        
        self.dubposA_chans = ttk.Entry(self.frame, width = 20)
        self.dubposA_chans.grid(row = 12, column = 2, columnspan = 2)
        
        self.dubposAthreshold_label = tk.Label(self.frame, text = 'Positive cell threshold:')
        self.dubposAthreshold_label.grid(row = 12, column = 4)
        
        self.dubposAthreshold = ttk.Entry(self.frame, width = 15,)
        self.dubposAthreshold.grid(row = 12, column = 5)
        
        
        self.var_dubposB = tk.IntVar()
        self.check_dubposB = tk.Checkbutton(self.frame, text = 'Multi-target transcript abundance', variable = self.var_dubposB)
        self.check_dubposB.grid(row = 13, column = 0)
        
        self.dubposB_chans_label = tk.Label(self.frame, text = 'Second set of multi-positive channels:')
        self.dubposB_chans_label.grid(row = 13, column = 1)
        
        self.dubposB_chans = ttk.Entry(self.frame, width = 20)
        self.dubposB_chans.grid(row = 13, column = 2, columnspan = 2) 
        
        self.dubposBthreshold_label = tk.Label(self.frame, text = 'Positive cell threshold:')
        self.dubposBthreshold_label.grid(row = 13, column = 4)
        
        self.dubposBthreshold = ttk.Entry(self.frame, width = 15)
        self.dubposBthreshold.grid(row = 13, column = 5)
        

        self.plot_button = tk.Button(self.frame, text = 'Commit selection', width = 25, command = self.plot_selector, bg = '#71C0A7')
        self.plot_button.grid(row = 14, column = 7)
        
    
        self.naminginput_header = tk.Label(self.frame, text = "Provide list of input dataset names and detection channel targets as they should appear on analysis outputs: ", font='Helvetica 9 bold')
        self.naminginput_header.grid(row = 18, columnspan = 2)
        
        self.chan_label = tk.Label(self.frame, text = 'Enter channel name list:')
        self.chan_label.grid(row = 19, column = 0)
        
        self.channel_names = ttk.Entry(self.frame, width = 30)
        self.channel_names.grid(row = 19, column = 1)
        
        self.dataset_label = tk.Label(self.frame, text = 'Enter dataset name list:')
        self.dataset_label.grid(row = 20, column = 0)
        
        self.dataset_names = ttk.Entry(self.frame, width = 30)
        self.dataset_names.grid(row = 20, column = 1)
        
        self.channel_button = tk.Button(self.frame, text = 'Commit lists', width = 25, command = self.chan_header_names, bg = '#71C0A7')
        self.channel_button.grid(row = 21, column = 7)
        
        self.run_button = tk.Button(self.frame, text = 'Run', width = 25, borderwidth = 5, command = self.run, bg = '#71C0A7')
        self.run_button.grid(row = 23, column = 7)
        
        
        
        
        self.frame.pack()
        
    def file_locator(self):
        location = self.folder.get()
        out = tk.Label(self.frame, text = f'Folder selected:   ...{location[-30:]}')
        out.grid(row = 3, column = 7)
        self.input_folder = repr(location.strip('"') +"/").strip("'")
        print(f'Input folder: {self.input_folder}')
        
    def plot_selector(self):
        self.hist = self.var_hist.get()
        self.scatter = self.var_scatter.get()
        self.expression = self.var_expression.get()
        self.dubposA = self.var_dubposA.get()
        self.dubposB = self.var_dubposB.get()
        
        if self.hist == 1:
            histout = tk.Label(self.frame, text = "Histogram")
            histout.grid(row = 7, column = 7)
            print("histogram")


        if self.scatter == 1:
            scatterout = tk.Label(self.frame, text = "Spatial Spot Distribution")
            scatterout.grid(row = 10, column = 7)
            print("scatter")
            if self.threshold.get() == "":
                self.Threshold = 1
            else:
                self.Threshold = self.threshold.get() 
        else:
            self.Threshold = 1
            
            
        if self.expression == 1:
            scatterout = tk.Label(self.frame, text = "Expression Analytics")
            scatterout.grid(row = 11, column = 7)
            print("RNA expression")
             
            
        if self.dubposA == 1:
            
            self.dpAchans = self.dubposA_chans.get()
            if self.dubposAthreshold.get() == "":
                self.dpAThreshold = 1
            else:
                self.dpAThreshold = self.dubposAthreshold.get()
            dubposAout = tk.Label(self.frame, text = f"Multi-Positive Analytics: {self.dpAchans[:12]}...")
            dubposAout.grid(row = 12, column = 7)
            print(f"First Multi-Positive Analytics: {self.dpAchans}")
        else:
            self.dpAchans = "Empty"
            self.dpAThreshold = 0
             
             
        if self.dubposB == 1:
            self.dpBchans = self.dubposB_chans.get()
            if self.dubposBthreshold.get() == "":
                self.dpBThreshold = 1
            else:
                self.dpBThreshold = self.dubposBthreshold.get()
            dubposBout = tk.Label(self.frame, text = f"Multi-Positive Analytics: {self.dpBchans[:12]}...")
            dubposBout.grid(row = 13, column = 7)
            print(f"Second Multi-Positive Analytics: {self.dpBchans}")
        else:
            self.dpBchans = "Empty"
            self.dpBThreshold = 0
        
        
        
             
        if self.hist == 0 and self.scatter == 0 and self.expression == 0 and self.dubposA == 0 and self.dubposB == 0:
            emptyout = tk.Label(self.frame, text = "Perform No Analysis")
            emptyout.grid(row = 13, column = 7)
            print("No Analysis")
        
        
    def chan_header_names(self):
        self.chan_headers = self.channel_names.get()
        self.dataset_labels = self.dataset_names.get()
        out = tk.Label(self.frame, text = f'Channel Names:  {self.chan_headers[:10]}...')
        out2 = tk.Label(self.frame, text = f'Datasets: {self.dataset_labels[:10]}...')
        out.grid(row = 19, column = 7)
        out2.grid(row = 20, column = 7)
        
        
        
    def run(self):
        self.master.destroy()

root = tk.Tk()
userinput = usrin(root)
root.mainloop()


#Runs FISHtoFigure by redirect
F2F.run(userinput.input_folder, userinput.hist, userinput.scatter, userinput.Threshold, userinput.expression, userinput.dubposA, userinput.dpAchans, userinput.dpAThreshold, userinput.dubposB, userinput.dpBchans, userinput.dpBThreshold, userinput.chan_headers, userinput.dataset_labels)
