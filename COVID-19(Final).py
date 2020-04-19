import tkinter as tk
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import pandas as pd
import ssl
import datetime
from PIL import ImageTk
from PIL import Image
import operator

class Parentclass(tk.Tk):
    #initiate the parent window
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        #create the container to contain all the frames
        container = tk.Frame(self)
        
        #as .pack puts everything in the middle, we use .grid to put whatever that 
        #is placed in the container to the left most
        container.grid(row = 0, column = 0)
        #create dictionary to contain the frames
        self.frames = {}
        
        frame = mainpage(container,self)
        
        self.frames[mainpage] = frame
        frame.grid(row = 0,column=0,sticky = 'nsew')
        self.show_frame(mainpage)
        
    def show_frame(self,framename):
        frametoshow = self.frames[framename]
        frametoshow.tkraise()
        
    #def plotconfirmedcases(self,countrylist,covidstatsconfirmed):
        
        
        
class mainpage(tk.Frame):
    def __init__(self,parent,controller):
        #create the frame for mainpage
        tk.Frame.__init__(self,parent)
        self.controller = controller
        
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
                      
        #while the mainpage object doesn't have the geometry attribute as it 
        #inherits from tk.Frame, mainpage 
        self.controller.geometry("1800x1050")
        self.controller.title('Covid-19 Tracker')
        self.region = tk.StringVar()
        self.region.set('Select Country/Region')
        
              
        
        self.radiobuttonframe = tk.LabelFrame(self, text = 'Select Visualization',bg = 'red4')
        self.radiobuttonframe.pack(side = 'left', anchor = 'nw', pady = 10,padx = 10, fill = 'y')
              
                
        #create 2 main frames to keep the other frames in
        self.largeframe = tk.LabelFrame(self, bg = 'red4')
        self.largeframe.pack(side = 'left')
        
        self.smallframe= tk.LabelFrame(self, bg = 'red4')
        self.smallframe.pack(side = 'left')
        
                                
        #confirmed case frame
        self.confirmedframe = tk.LabelFrame(self.largeframe)
        self.confirmedframe.pack( side = 'top',pady = 10, padx = 10, anchor = 'nw')
        
        #relative case container
        self.relativeframe = tk.LabelFrame(self.largeframe)
        self.relativeframe.pack(side = 'top',pady = 10, padx = 10, anchor = 'w', fill = 'x')
        
        self.deathframe = tk.LabelFrame(self.smallframe)
        self.deathframe.pack(side = 'top',pady = 10, padx = 10, anchor = 'ne')
        
        #recoveredcaseframe
        self.recoveredframe = tk.LabelFrame(self.smallframe)
        self.recoveredframe.pack(side = 'top',pady = 10, padx = 10)
        
        #create containers which act like empty sheets
        #where you can place the canvas on 
        #making a confirmed canvas container to put the canvas in
        #NOTICE THE CONTAINERS ARE ASSIGNED UNDER THE 
        #PREVIOUSLY BUILT FRAMES
        confirmedcontainer = tk.Frame(self.confirmedframe)
        increasecontainer = tk.Frame(self.relativeframe)
        deathcontainer = tk.Frame(self.deathframe)
        recoveredcontainer = tk.Frame(self.recoveredframe)
        
        confirmedcontainer.grid(row = 1,column = 0)
        increasecontainer.grid(row = 1, column = 0)
        deathcontainer.grid(row = 1,column = 0)
        recoveredcontainer.grid(row = 1, column = 0)
     
        #making the figures and subplots
        self.fconfirmed = Figure(figsize = (7.5,4.725),dpi = 100)
        self.aconfirmed = self.fconfirmed.add_subplot(111)
        self.aconfirmed.set_xlabel('Date')
        self.aconfirmed.set_ylabel('Number of Cases')
        self.aconfirmed.set_title('Confirmed Cases')
        
                
        #placing the axes for relative cases
        self.fincrease = Figure(figsize = (7.5,4.725),dpi = 100)
        self.aincrease = self.fincrease.add_subplot(111)
        self.aincrease.set_xlabel('Date')
        self.aincrease.set_ylabel('Increase in cases')
        self.aincrease.set_title('Daily increase in cases')

        
        
        #placing the axes for deaths
        self.fdeath = Figure(figsize = (7.5,4.725),dpi = 100)
        self.adeath = self.fdeath.add_subplot(111)
        self.adeath.set_xlabel('Date')
        self.adeath.set_ylabel('Number of Deaths')
        self.adeath.set_title('Deaths')

        
        
        #placing axes for recovered cases
        self.frecovered = Figure(figsize = (7.5,4.725),dpi = 100)
        self.arecovered = self.frecovered.add_subplot(111)
        self.arecovered.set_xlabel('Date')
        self.arecovered.set_ylabel('Number of Recoveries')
        self.arecovered.set_title('Recovered Cases')

        
        axeslist = [self.aconfirmed,self.aincrease,self.adeath,self.arecovered]
        
        for axes in axeslist:
            for label in axes.xaxis.get_ticklabels():
                label.set_rotation(0)
        
        #putting grids on axes
        self.aconfirmed.grid()
        self.aincrease.grid()
        self.adeath.grid()
        self.arecovered.grid()
        

        
        #the figure is placed on the container template
        #create the canvases
        canvasconfirmed = FigureCanvasTkAgg(self.fconfirmed,confirmedcontainer)
        canvasconfirmed.draw()
        #packs the canvas onto the container
        canvasconfirmed.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        
        canvasincrease = FigureCanvasTkAgg(self.fincrease, increasecontainer)
        canvasincrease.draw()
        #packs the canvas onto the container
        canvasincrease.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        
        canvasdeath = FigureCanvasTkAgg(self.fdeath,deathcontainer)
        canvasdeath.draw()
        #packs the canvas onto the container
        canvasdeath.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        
        canvasrecovered = FigureCanvasTkAgg(self.frecovered,recoveredcontainer)
        canvasrecovered.draw()
        #packs the canvas onto the container
        canvasrecovered.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        
        #making a toolbar container to put into the confirmedframe
        frameandcanvas = [(self.confirmedframe,canvasconfirmed),(self.relativeframe,canvasincrease),\
                          (self.deathframe,canvasdeath),(self.recoveredframe,canvasrecovered)]
        for element in frameandcanvas:
            toolbarframe = tk.Frame(element[0])
            toolbarframe.grid(row = 2, column = 0,sticky = 'w')
            #placing the toolbar on the canvas
            toolbar = NavigationToolbar2Tk(element[1],toolbarframe)
            
        #list to contain all selected cases
        self.confirmedcaselist = list()
        self.increasecaselist = list()
        self.deathcaselist = list()
        self.recoveredcaselist = list()
        
        #option menu containing cases
        self.countrylist = tk.OptionMenu(self.radiobuttonframe,self.region,())
        self.countrylist.grid(row = 1, column = 1, padx = 10,pady = 10)
        
        #confirmedcases
        csvconfirmedurl = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
        self.covidstatsconfirmed = pd.read_csv(csvconfirmedurl)
        self.countries = self.covidstatsconfirmed['Country/Region'].unique().tolist()
        
        #deaths
        csvdeathsurl = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
        self.covidstatsdeaths = pd.read_csv(csvdeathsurl)
        
        #recovered
        csvrecoveredurl = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
        self.covidstatsrecovered = pd.read_csv(csvrecoveredurl)
        
        
        menu = self.countrylist['menu']
        menu.delete(0,'end')
        for country in self.countries:
            menu.add_command(label = country, command = lambda value = country:self.region.set(value))
            

        
        #button to plot countries
        self.plotconfcases = tk.Button(self.radiobuttonframe, text = 'Plot Confirmed Cases', command = lambda: self.plotconfirmed(self.region.get(),\
                                                                                                                                  self.covidstatsconfirmed,\
                                                                                                                                  canvasconfirmed))
        self.plotconfcases.grid(row = 2, column = 1, padx = 10, pady = 10)
        
        self.plotdeathcases = tk.Button(self.radiobuttonframe, text = 'Plot Deaths', command = lambda: self.plotdeath(self.region.get(),\
                                                                                                                      self.covidstatsdeaths,\
                                                                                                                      canvasdeath))
        self.plotdeathcases.grid(row = 3, column = 1, padx = 10, pady = 10)
        
        self.plotrecoveredcases = tk.Button(self.radiobuttonframe, text = 'Plot Recovered Cases', command = lambda: self.plotrecovered(self.region.get(),\
                                                                                                                      self.covidstatsrecovered,\
                                                                                                                      canvasrecovered))
        self.plotrecoveredcases.grid(row = 4, column = 1, padx = 10, pady = 10)
        
        self.plotcaseincrease = tk.Button(self.radiobuttonframe, text = 'Plot Increase in Cases', command = lambda: self.plotincrease(self.region.get(),\
                                                                                                                                       self.covidstatsconfirmed,\
                                                                                                                                       canvasincrease))
        
        self.plotcaseincrease.grid(row = 5, column = 1, padx = 10, pady = 10)
        
        
        self.deleteconfirmedcases = tk.Button(self.radiobuttonframe, text = 'Delete Selected Plot from Confirmed Cases', command = lambda: \
                                                                                                                          self.deletecase(self.region.get(),canvasconfirmed,\
                                                                                                                                    self.aconfirmed, self.aconfirmed2dlinedict))
        self.deleteconfirmedcases.grid(row = 6, column = 1, padx = 10, pady = 10)
        
        
        self.deletedeathcase = tk.Button(self.radiobuttonframe, text = 'Delete Selected Plot from Deaths', command = lambda: \
                                                                                                             self.deletecase(self.region.get(),canvasdeath,\
                                                                                                                                  self.adeath, self.adeath2dlinedict))
        self.deletedeathcase.grid(row = 7, column = 1, padx = 10, pady = 10)
        
        
        self.deleterecoverycase = tk.Button(self.radiobuttonframe, text = 'Delete Selected Plot from Recovered Cases', command = lambda: \
                                                                                                             self.deletecase(self.region.get(),canvasrecovered,\
                                                                                                                                  self.arecovered, self.arecovered2dlinedict))
        self.deleterecoverycase.grid(row = 8, column = 1, padx = 10, pady = 10)

        
        self.resetbutton = tk.Button(self.radiobuttonframe, text = 'Reset all Graphs', command = lambda: \
                                                                                         self.resetall(self.aconfirmed,self.adeath,self.arecovered, \
                                                                                         self.aconfirmed2dlinedict, \
                                                                                         self.adeath2dlinedict, \
                                                                                         self.arecovered2dlinedict, \
                                                                                         self.confirmedcaselist, \
                                                                                         self.deathcaselist, \
                                                                                         self.recoveredcaselist, \
                                                                                         canvasconfirmed, canvasdeath, canvasrecovered))
        self.resetbutton.grid(row = 9, column = 1, padx = 10, pady = 10)
    
        #adding image onto label in the radio button frame
        img = ImageTk.PhotoImage(Image.open(r'C:\Users\ASUS\Desktop\Python code\Covid\covidimage.jpg'))
        self.imagelabel = tk.Label(self.radiobuttonframe, image = img)
        self.imagelabel.image = img
        self.imagelabel.grid(row = 10, column = 1, padx = 10, pady = 10)
        
    
    
    
        #dates in date format
        self.datesstringformat = list(self.covidstatsconfirmed.columns.values)[4:]
        self.datesforplotting = list(map(datetime.datetime.strptime,self.datesstringformat,len(self.datesstringformat)*['%m/%d/%y']))
        
        #creating a dictionary to place the subplots 2d line classes for each
        #country    
        self.aconfirmed2dlinedict = dict()
        self.aincrease2dlinedict = dict()
        self.adeath2dlinedict = dict()
        self.arecovered2dlinedict = dict()
    
    def plotconfirmed(self, country,covidstatsconfirmed,canvasconfirmed):
        if country not in self.confirmedcaselist:
            self.confirmedcaselist.append(country)
            countrydata = covidstatsconfirmed.loc[lambda covidstatsconfirmed:covidstatsconfirmed['Country/Region'] == country]
            countryplotdata = countrydata[self.datesstringformat].sum()
            self.aconfirmed.plot_date(self.datesforplotting,countryplotdata,'-',label = country)
            self.aconfirmed2dlinedict[country] = self.aconfirmed.lines[-1]
            confirmedhandles,confirmedlegend = self.aconfirmed.get_legend_handles_labels()
            self.aconfirmed.legend(confirmedhandles,confirmedlegend)
            #if self.confirmed.legend() is placed after the canvasconfirmed codes, given that 
            #canvas confirmed is already a result of placing the figure on the container 
            #template, the legend needs to be defined first so it applies to the canvasconfirmed
            #instance
            canvasconfirmed.draw()
            canvasconfirmed.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        else:
            tk.messagebox.showinfo('Attention','Already Displayed on Confirmed Cases Plot')
    
    def plotdeath(self,country,covidstatsdeath,canvasdeath):
        if country not in self.deathcaselist:
            self.deathcaselist.append(country)
            countrydata = covidstatsdeath.loc[lambda covidstatsdeath:covidstatsdeath['Country/Region'] == country]
            countryplotdata = countrydata[self.datesstringformat].sum()
            self.adeath.plot_date(self.datesforplotting,countryplotdata,'-',label = country)
            self.adeath2dlinedict[country] = self.adeath.lines[-1]
            deathhandles,deathlabels = self.adeath.get_legend_handles_labels()
            self.adeath.legend(deathhandles,deathlabels)
            canvasdeath.draw()
            canvasdeath.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        else:
            tk.messagebox.showinfo('Attention','Already Displayed on Deaths Plot')
            
    
    def plotrecovered(self,country,covidstatrecovered,canvasrecovered):
        if country not in self.recoveredcaselist:
            self.recoveredcaselist.append(country)
            countrydata = covidstatrecovered.loc[lambda covidstatrecovered:covidstatrecovered['Country/Region'] == country]
            countryplotdata = countrydata[self.datesstringformat].sum()
            self.arecovered.plot_date(self.datesforplotting,countryplotdata,'-',label = country)
            self.arecovered2dlinedict[country] = self.arecovered.lines[-1]
            recoveredhandles,recoveredlabels = self.arecovered.get_legend_handles_labels()
            self.arecovered.legend(recoveredhandles,recoveredlabels)
            canvasrecovered.draw()
            canvasrecovered.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        else:
            tk.messagebox.showinfo('Attention','Already Displayed on Recovered Cases Plot')
        
    def plotincrease(self, country, covidstatsconfirmed, canvasincrease):
        if country not in self.increasecaselist:
            self.increasecaselist.append(country)
            countrydata = covidstatsconfirmed.loc[lambda covidstatsconfirmed:covidstatsconfirmed['Country/Region'] == country]
            countryrawdatafullset = countrydata[self.datesstringformat].sum()
            #starting date is one day after initial day of 22 Jan 2019
            datesubset = self.datesstringformat[1:]
            #create a subset of data to calculate the difference in case number each day
            countryrawdatasubset = countrydata[datesubset].sum()
            #finding the difference between consequent dates
            increases = list(map(operator.sub,countryrawdatasubset,countryrawdatafullset[:-1]))
            #pos = [i for i, f in enumerate(dailyincreases) if f < 0]
            #as there can be negative values(decrease in number of cases), we set these to zero 
            dailyincreases = [i - i if i < 0 else i for i in increases]
            self.aincrease.plot_date(self.datesforplotting[1:], dailyincreases,'-', label = country)
            increasehandles,increaselabels = self.aincrease.get_legend_handles_labels()
            self.aincrease2dlinedict[country] = self.aincrease.lines[-1]
            self.aincrease.legend(increasehandles, increaselabels, loc = 'upper left')
            canvasincrease.draw()
            canvasincrease.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        else:
            tk.messagebox.showinfo('Attention','Already Displayed on Plot')
        
    
    #country is the result of self.region.get()        
    #canvas is the result for FigureCanvasTkAgg
    #axesname is the instance from add2subplot
    #twolinedict is the dictionary holding the 2dline handle for each plot line
    def deletecase(self,country,canvas,axesname,twodlinedict):
        handles,labels = axesname.get_legend_handles_labels()
        if country in labels:
            axesname.lines.remove(twodlinedict[country])
            handlesafterpltremove,labelsafterpltremove = axesname.get_legend_handles_labels()
            axesname.legend(handlesafterpltremove,labelsafterpltremove, loc = 'upper left')
            canvas.draw()
            canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        else:
            tk.messagebox.showinfo('Attention','Plot is not available on plot for deletion')
    
    def resetall(self,confirmedplot, deathplot, recoveredplot, confirmedtwodlinedict, deathtwodlinedict,recoveredtwodlinedict,\
                 confirmedcases,deathcases, recoveredcases, canvasconfirmed, canvasdeath, canvasrecovered):
        confirmedlabels = confirmedplot.get_legend_handles_labels()[1]
        deathlabels = deathplot.get_legend_handles_labels()[1]
        recoveredlabels = recoveredplot.get_legend_handles_labels()[1]
        if len(confirmedlabels) > 0 or len(deathlabels) > 0 or len(recoveredlabels) > 0:
            for axs in (confirmedplot, deathplot, recoveredplot):
                axs.lines.clear()
            for dictionaries in (confirmedtwodlinedict, deathtwodlinedict,recoveredtwodlinedict):
                dictionaries.clear()
            for lists in (confirmedcases, deathcases, recoveredcases):
                lists.clear()
            for canvas in (canvasconfirmed, canvasdeath, canvasrecovered):
                canvas.draw()
                canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        else:
            tk.messagebox.showinfo('Attention','No plots available to reset')
        

      
        

    
        
       








root = Parentclass()
root.mainloop()