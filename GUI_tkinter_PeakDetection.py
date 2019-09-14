
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# Implement the default Matplotlib key bindings.
#from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk

import urllib
import json

import pandas as pd
import numpy as np

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)
style.use("ggplot")

f = Figure(figsize=(10, 6), dpi=100)
a = f.add_subplot(111)
#b = f.add_subplot(211)

#Pop up message function
def popupmsg(msg):
    popup = tk.Tk()      
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

#Animation matplotlib, this code populate the data
def animate(i):
    pullData = open('EOG01_blink_pre_with_time_col.txt').read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine)>1:
            x, y = eachLine.split(',')
            xList.append(float(x))
            yList.append(float(y))
#   Clear everything in the subplot for keeping graph clear.
    a.clear()
    a.plot(xList, yList)
    #a.scatter(xList, yList)

    # Second graph
    pullData1 = open('EOG01_blink_pre_with_time_col2.txt').read()
    dataList1 = pullData1.split('\n')
    xList1 = []
    yList1 = []
    for eachLine in dataList1:
        if len(eachLine)>1:
            x1, y1 = eachLine.split(',')
            xList1.append(float(x1))
            yList1.append(float(y1))
#   Clear everything in the subplot for keeping graph clear.
    #b.clear()
    #b.plot(xList, yList)
    a.scatter(xList1, yList1, color="b")
            

class EOG_Peak_detector(tk.Tk):
# CODE FOR INITIAL PAGE SET UP
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        
        #Code for changing icon
        tk.Tk.iconbitmap(self, default="signal.ico")
        tk.Tk.wm_title(self, "EOG_Peak_detector")
        
        #Container set up
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #Menu bar container
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command = lambda: popupmsg("Not supported just yet"))
        #For separeting options in menu bar
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        # For displaying minibar
        menubar.add_cascade(label="File", menu=filemenu)

        tk.Tk.config(self, menu=menubar)

        self.frames = {}
        #LOOP FOR NAVIGATION BETWEEN PAGES
        for F in (StartPage, PeakDetectorPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            self.show_frame(StartPage)

    def show_frame(self, cont):

            frame = self.frames[cont]
            frame.tkraise()
# CODE WHICH SUGGEST HOW TO MAKE A NEW PAGES AND NAVIGATE
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text=("""Welcome to EOG - Alpha peak detector app. This product is not ready yet."""), font=LARGE_FONT)
        label.pack(pady=80,padx=40)

        button = ttk.Button(self, text="Show Detected Peaks",
                           command=lambda: controller.show_frame(PeakDetectorPage))
        button.pack()

        button2 = ttk.Button(self, text="Exit",
                            command=quit)
        button2.pack()

#TEMPLATE FOR PAGE ONE!
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start One!", font=LARGE_FONT)
        label.pack(pady=20,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        
class PeakDetectorPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=20,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()



        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        
    
app = EOG_Peak_detector()
app.geometry("1280x720")
ani = animation.FuncAnimation(f, animate, interval=5000)
app.mainloop()
