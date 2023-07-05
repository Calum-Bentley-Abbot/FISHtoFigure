# -*- coding: utf-8 -*-
"""
FISHtoFigure GUI, allows for input folder selection by path, the selection of analysis options
and the specification of flags and dataset names for plotting
"""

import tkinter as tk

from threading import Thread
import time

import FISHtoFigure_v101_main as F2F

class usrin():
    def __init__(self, master):   
        self.master = master
        master.title("FISHtoFigure")
        master.geometry('1180x530')
        self.frame = tk.Frame(self.master)
        self.frame.grid_rowconfigure(1, minsize = 40)
        self.frame.grid_rowconfigure(5, minsize = 20)
        self.frame.grid_rowconfigure(15, minsize = 20)
        self.frame.grid_rowconfigure(18, minsize = 20)
        self.frame.grid_rowconfigure(22, minsize = 10)
        self.frame.grid_rowconfigure(25, minsize = 10)
        self.frame.grid_columnconfigure(4, minsize = 150)
        self.frame.grid_columnconfigure(6, minsize = 10)
        self.frame.grid_columnconfigure(7, minsize = 200)
        
        
        self.main_header = tk.Label(self.frame, text = 'Welcome to FISHtoFigure, please seperate names in channel and dataset lists with a comma and single space', font='Helvetica 9 bold', width=128, anchor='w')
        self.main_header.grid(row = 0, column=0, columnspan = 6)
        
        self.analysis_header = tk.Label(self.frame, text = 'Provide path to input data directory:', font='Helvetica 9 bold', width=30, anchor='w')
        self.analysis_header.grid(row = 1, column = 0)
        
        
        self.in_label = tk.Label(self.frame, text = 'Enter Input Folder path:', width = 29, anchor = 'w')
        self.in_label.grid(row = 3, column = 0)
            
        self.folder = tk.Entry(self.frame, width = 35, borderwidth = 5)
        self.folder.grid(row = 3, column = 1)
            
        self.folder_button = tk.Button(self.frame, text = 'Find', width = 20, command = self.file_locator, bg = '#71C0A7')
        self.folder_button.grid(row = 4, column = 7)
        
        
        self.box_header = tk.Label(self.frame, text = 'Select analysis options:', font='Helvetica 9 bold', width = 30, anchor='w')
        self.box_header.grid(row = 6, column = 0)
            
        self.var_hist = tk.IntVar()
        self.check_hist = tk.Checkbutton(self.frame, text = 'Plot transcript occurances', variable = self.var_hist, width = 26, anchor = 'w')
        self.check_hist.grid(row = 7, column = 0)
 
        self.var_scatter = tk.IntVar()
        self.check_scatter = tk.Checkbutton(self.frame, text = 'Plot transcript distribution', variable = self.var_scatter, width = 26, anchor = 'w')
        self.check_scatter.grid(row = 10, column = 0)
        
        self.threshold_label = tk.Label(self.frame, text = 'Positive cell threshold:', width=20, anchor='e')
        self.threshold_label.grid(row = 10, column = 4)
        
        self.threshold = tk.Entry(self.frame, width = 10, borderwidth = 5)
        self.threshold.grid(row = 10, column = 5)
        
        self.var_expression = tk.IntVar()
        self.check_expression = tk.Checkbutton(self.frame, text = 'Transcript abundance analysis', variable = self.var_expression, width = 26, anchor = 'w')
        self.check_expression.grid(row = 11, column = 0)
        
        
        
        
        self.var_dubposA = tk.IntVar()
        self.check_dubposA = tk.Checkbutton(self.frame, text = 'Multi-target transcript abundance', variable = self.var_dubposA, width = 26, anchor = 'w')
        self.check_dubposA.grid(row = 12, column = 0)
        
        self.dubposA_chans_label = tk.Label(self.frame, text = 'First set of multi-positive channels:', width = 40, anchor = 'e')
        self.dubposA_chans_label.grid(row = 12, column = 1)
        
        self.dubposA_chans = tk.Entry(self.frame, width = 25, borderwidth = 5)
        self.dubposA_chans.grid(row = 12, column = 2)
        
        self.dubposAthreshold_label = tk.Label(self.frame, text = 'Positive cell threshold:', width=20, anchor='e')
        self.dubposAthreshold_label.grid(row = 12, column = 4)
        
        self.dubposAthreshold = tk.Entry(self.frame, width = 10, borderwidth = 5)
        self.dubposAthreshold.grid(row = 12, column = 5)
        
        
        self.var_dubposB = tk.IntVar()
        self.check_dubposB = tk.Checkbutton(self.frame, text = 'Multi-target transcript abundance', variable = self.var_dubposB, width = 26, anchor = 'w')
        self.check_dubposB.grid(row = 13, column = 0)
        
        self.dubposB_chans_label = tk.Label(self.frame, text = 'Second set of multi-positive channels:', width = 40, anchor = 'e')
        self.dubposB_chans_label.grid(row = 13, column = 1)
        
        self.dubposB_chans = tk.Entry(self.frame, width = 25, borderwidth = 5)
        self.dubposB_chans.grid(row = 13, column = 2) 
        
        self.dubposBthreshold_label = tk.Label(self.frame, text = 'Positive cell threshold:', width=20, anchor='e')
        self.dubposBthreshold_label.grid(row = 13, column = 4)
        
        self.dubposBthreshold = tk.Entry(self.frame, width = 10, borderwidth = 5)
        self.dubposBthreshold.grid(row = 13, column = 5)
        

        self.plot_button = tk.Button(self.frame, text = 'Commit selection', width = 20, command = self.plot_selector, bg = '#71C0A7')
        self.plot_button.grid(row = 14, column = 7)
        
    
        self.naminginput_header = tk.Label(self.frame, text = "Provide list of input dataset names and detection channel targets as they should appear on analysis outputs: ", font='Helvetica 9 bold', width = 96, anchor = 'w')
        self.naminginput_header.grid(row = 18, columnspan = 4)
        
        self.chan_label = tk.Label(self.frame, text = 'Enter channel name list:', width = 29, anchor = 'w')
        self.chan_label.grid(row = 19, column = 0)
        
        self.channel_names = tk.Entry(self.frame, width = 35, borderwidth = 5)
        self.channel_names.grid(row = 19, column = 1)
        
        self.dataset_label = tk.Label(self.frame, text = 'Enter dataset name list:', width = 29, anchor = 'w')
        self.dataset_label.grid(row = 20, column = 0)
        
        self.dataset_names = tk.Entry(self.frame, width = 35, borderwidth = 5)
        self.dataset_names.grid(row = 20, column = 1)
        
        self.channel_button = tk.Button(self.frame, text = 'Commit lists', width = 20, command = self.chan_header_names, bg = '#71C0A7')
        self.channel_button.grid(row = 21, column = 7)
        
        self.run_button = tk.Button(self.frame, text = 'Run', width = 20, command = self.threading, bg = '#42F9F9')
        self.run_button.grid(row = 23, column = 7)
        
        self.quit_button = tk.Button(self.frame, text = 'Quit', width = 6, command = self.quitprogram, bg = '#71C0A7')
        self.quit_button.grid(row = 26, column = 7, padx=(100,0))
        
        
        self.frame.pack()
        
    def file_locator(self):
        location = self.folder.get()
        out = tk.Label(self.frame, text = f'Path: ...{location[-16:]}')
        out.grid(row = 3, column = 7)
        self.input_folder = repr(location.strip('"') +"\\").strip("'")
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
            scatterout = tk.Label(self.frame, text = "Spot Distribution")
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
            dubposAout = tk.Label(self.frame, text = f"Analytics: {self.dpAchans[:12]}...")
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
            dubposBout = tk.Label(self.frame, text = f"Analytics: {self.dpBchans[:12]}...")
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
        out = tk.Label(self.frame, text = f'Channels:  {self.chan_headers[:10]}...')
        out2 = tk.Label(self.frame, text = f'Datasets: {self.dataset_labels[:10]}...')
        out.grid(row = 19, column = 7)
        out2.grid(row = 20, column = 7)
        

    def threading(self):
        t = Thread(target=self.run)
        t.start()
        
    def run(self):
        info = tk.Label(self.frame, text = "Running")
        info.grid(row = 23, column = 5)
        time.sleep(1)
        #Runs FISHtoFigure by redirect
        F2F.run(zstack.input_folder, zstack.hist, zstack.scatter, zstack.Threshold, zstack.expression, zstack.dubposA, zstack.dpAchans, zstack.dpAThreshold, zstack.dubposB, zstack.dpBchans, zstack.dpBThreshold, zstack.chan_headers, zstack.dataset_labels)
        time.sleep(1)
        info.configure(text = "Finished")
    
    def quitprogram(self):    
        self.master.destroy()

root = tk.Tk()
zstack = usrin(root)
root.mainloop()


