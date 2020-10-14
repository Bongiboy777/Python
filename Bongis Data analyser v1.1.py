'''
Bongis Data analyser script v1.1
Author: Bongani Luwemba
Version 1.1
Date: 11/10/20
'''
import os;
import tkinter as tk;
import urllib.request;
import urllib3;
import opendatasets as od;
import jovian;
import numpy as np;
import pandas as pd;
import seaborn as sns;
import matplotlib;
import matplotlib.pyplot as plt;
import math;
#%matplotlib inline
import kaggle;
import math;
kaggle.api.authenticate();

############################################################
#Initial global variables
############################################################

owners = dict(); # list of username tags for file search
filerequests = []; # document belonging to owner, to download
fullrequest = []; # full address of document, i.e kaggle/owner/filerequest
File_count = 0; # Count for number of requests/folders downloaded
InitialPath = os.getcwd()+"\\DataFiles\\" # initial path to store folders
folderuibuttons = []
owneruibuttons = []
fileuibuttons = []
columnbutton = []
toggledbuttons = []
df_buttons = []
numberrangelabels = []
wordrangelabels = []
wordchecks = []
plotbuttons = []
dfranges = []
xybuttonstate = 0
plotbuttonstate = 0
Plotoptions = ["Histogram", "Simpplot", "Scatter","ScatterPlot", "Bar","BarPlot"]
x = dict()
WIDTH = 800
HEIGHT = 800

############################################################
#Initialise gui 
############################################################

global select_root
select_root = tk.Tk();

#check_directory("","",0)
global canvas
canvas = tk.Canvas(select_root, height = HEIGHT, width = WIDTH);
canvas.pack()

Title = tk.Label(canvas, text = "Bongs data analyser")
Title.place(relwidth = 0.7, relheight = 0.05, relx = 0.15, rely = 0.0)

#This frame and its contents are used to add a new dataframe by owner and folder name
global frame_1
frame_1 = tk.Frame(canvas, bg = "red");
frame_1.place(relwidth = 0.9, relheight = 0.2, relx = 0.05, rely = 0.05)

select_frame_2 = tk.Frame(canvas, bg = "blue");
select_frame_2.place(relwidth = 0.45, relheight = 0.70, relx = 0.05, rely = 0.30)

select_frame_3 = tk.Frame(canvas, bg = "green");
select_frame_3.place(relwidth = 0.45, relheight = 0.7, relx = 0.5, rely = 0.30)

tempframe = tk.Frame(canvas, bg = "yellow")

Ownerentrylabel = tk.Label(frame_1, text = "Enter dataframe owner, e.g drgilermo")
Ownerentrylabel.place(relwidth = 3/9, relheight = 2/9, relx = 1/9, rely = 1/9)
Ownerentry = tk.Entry(frame_1, text = "drgilermo")
Ownerentry.place(relwidth = 3/9, relheight = 1/3, relx = 1/9, rely = 1/3)

Datalabel = tk.Label(frame_1, text = "Enter Data name, e.g nba-players-stats")
Datalabel.place(relwidth = 3/9, relheight = 2/9, relx = 5/9, rely = 1/9)
Dataentry = tk.Entry(frame_1, text = "nba-players-stats")
Dataentry.place(relwidth = 3/9, relheight = 1/3, relx = 5/9, rely = 1/3)

Add_File_button = tk.Button(frame_1, text = "Add files", command = lambda:[NewReqest(Ownerentry.get(),Dataentry.get()),ownersui()]);
Add_File_button.place(relwidth = 1/5, relheight = 1/5, relx = 2/5, rely = 4/5)

Prompt = tk.Label(canvas, bg = "yellow", text = "To start, add a csv based data set by owner and dataset name")
Prompt.place(relwidth = 0.9, relheight = 0.05, relx = 0.05, rely = 0.25)

close = tk.Button(canvas, text = "exit", command = lambda:[close_window(select_root, owneruibuttons)], bg = "red");
close.place(relwidth = 1/20, relheight = 0.05, relx = 0.9, rely = 0.25)


############################################################
#Dataframe Functions
############################################################
def returnquery(dataframe):
    
    if not toggledbuttons:
        return dataframe


    elif len(toggledbuttons) == 1:
        for button in toggledbuttons:
            column = button["text"]
            try:
                if dataframe[column].dtype  == "float64":
                    if x[column]["from"].get() == '' or x[column]["from"].get() == '':
                        if x[column]["from"].get() == '':
                            From = dataframe[column].min()
                        if x[column]["from"].get() == '':
                            To = dataframe[column].max()
                    else:
                        From = float(x[column]["from"].get())
                        To = float(x[column]["to"].get())

                    mod = (dataframe[column].between(From,To))
                    return dataframe[mod].sort_values(column)
                    print("This Query has {} entries".format(dataframe[mod].shape[0])) 
            
                elif dataframe[column].dtype  == "int64":
                    if x[column]["from"].get() == '' or x[column]["from"].get() == '':
                        if x[column]["from"].get() == '':
                            From = dataframe[column].min()
                        if x[column]["from"].get() == '':
                            To = dataframe[column].max()
                    else:
                        From = float(x[column]["from"].get())
                        To = float(x[column]["to"].get())

                    mod = (dataframe[column].between(From,To))
                    return dataframe[mod].sort_values(column)
                    print("This Query has {} entries".format(dataframe[mod].shape[0])) 

                elif dataframe[column].dtype  == "O":
                    if x[column]["Entry"].get() == "":
                        print("This Query has {} entries".format(dataframe.shape[0])) 
                        return dataframe.sort_values(column)
                        
                    else:
                        Entry = x[column]["Entry"].get()
                        mod = (dataframe[column] == Entry)
                        return dataframe[mod].sort_values(column)
                        print("This Query has {} entries".format(dataframe[mod].shape[0])) 

                elif dataframe[column].dtype  == "bool":
                    if x[column]["B"]["bg"] == "red":
                        mod = (dataframe[column] == False)
                        return dataframe[mod].sort_values(column)
                        print("This Query has {} entries".format(dataframe[mod].shape[0])) 
                        
                    elif x[column]["B"]["bg"] == "yellow":
                        mod = (dataframe[column] == True)
                        return dataframe[mod].sort_values(column)
                        print("This Query has {} entries".format(dataframe[mod].shape[0])) 
                    else:
                        return dataframe.sort_values(column)
            except:
                Prompt.config(text = "{} entry is invalid".format(column))

    else:
        base = True
        for button in toggledbuttons:
            column = button["text"]
            try:
                if dataframe[column].dtype  == "float64":
                    if x[column]["from"].get() == '' or x[column]["from"].get() == '':
                        if x[column]["from"].get() == '':
                            From = dataframe[column].min()
                        if x[column]["from"].get() == '':
                            To = dataframe[column].max()
                    else:
                        From = float(x[column]["from"].get())
                        To = float(x[column]["to"].get())
                        mod = (dataframe[column].between(From,To))
                        base = base & mod
                    
                elif dataframe[column].dtype  == "int64":
                    if x[column]["from"].get() == '' or x[column]["from"].get() == '':
                        if x[column]["from"].get() == '':
                            From = dataframe[column].min()
                        if x[column]["from"].get() == '':
                            To = dataframe[column].max()
                    else:
                        From = int(x[column]["from"].get())
                        To = int(x[column]["to"].get())
                        mod = (dataframe[column].between(From,To))
                        base = base & mod

                elif dataframe[column].dtype  == "O":
                    if x[column]["Entry"].get() == "":
                        pass;
                    else:
                        Entry = x[column]["Entry"].get()
                        mod = (dataframe[column] == Entry)
                        base = base & mod


                elif dataframe[column].dtype  == "bool":

                    if x[column]["B"]["bg"] == "red":
                        mod = (dataframe[column] == False)
                        base = base & mod
                        
                    elif x[column]["B"]["bg"] == "yellow":
                        mod = (dataframe[column] == True)
                        base = base & mod
            except:
                Prompt.config(text = "{} entry is invalid".format(column))

        if type(base) is bool:
            return dataframe
            
        else:
            return dataframe[base]
            print("This Query has {} entries".format(dataframe[base].shape[0]))  

def showdata(dataframe):
    print(dataframe)

def shape(dataframe):
    if not toggledbuttons:
        print("This file has {} rows and {} columns.".format(dataframe.shape[0],dataframe.shape[1]))
    else:
        fb = []
        for button in toggledbuttons:
            fb.append(button["text"])

        print("This query has {} rows and {} columns.".format(dataframe[fb].shape[0],dataframe[fb].shape[1]))
        
def Describe(dataframe,column):
    Sum = dataframe[column].sum()
    Range = dataframe[column].max() - dataframe[column].min()
    mean = dataframe[column].mean()
    cumsum = dataframe[column].cumsum()
    
    print("{} description:\nSum\t{}\nMean\t{}\nRange\t{}".format(column, Sum, mean,Range))

def DescribeExisting(dataframe,column):
    values = dataframe[column].unique()
    print("Values in {} column:\n{}".format(column, values))
    
############################################################
#Dataframe Range Functions
############################################################

def makerange(dataframe, column):
    place = 1.2*(len(x) +1)
    if dataframe[column].dtype == "O":
        d = dict()
        d["describe"] = tk.Button(select_frame_3, bg = "purple", text = "Describe", command = lambda:DescribeExisting(returnquery(dataframe),column))
        d["describe"].place(relwidth = 26/81, relheight = 1/20, relx = 55/81, rely = place/20)
        d["Entry"] = tk.Entry(select_frame_3, bg = "purple")
        d["Entry"].place(relwidth = 1/3, relheight = 1/20, relx = 1/3, rely = place/20)
        d["title"] = tk.Label(select_frame_3, text = column, bg = "green")
        d["title"].place(relwidth = 1/3, relheight = 1/20, relx = 0, rely = place/20)
        x[column] = d

    elif dataframe[column].dtype == "int64" or dataframe[column].dtype == "float64":
        #print("number\t{}".format(dataframe[column].dtype))
        
        d = dict()
        d["describe"] = tk.Button(select_frame_3, bg = "purple", text = "Describe", command = lambda:Describe(returnquery(dataframe),column))
        d["describe"].place(relwidth = 26/81, relheight = 1/20, relx = 55/81, rely = place/20)
        d["from"] = tk.Entry(select_frame_3, bg = "purple")
        d["to"] = tk.Entry(select_frame_3, bg = "purple")
        d["from"].place(relwidth = 1/9, relheight = 1/20, relx = 1/3, rely = place/20)
        d["to"].place(relwidth = 1/9, relheight = 1/20, relx = 5/9, rely = place/20)
        d["To"] = tk.Label(select_frame_3, bg = "green", text = "to".format(column))
        d["To"].place(relwidth = 1/9, relheight = 1/20, relx = 4/9, rely = place/20)
        d["title"] = tk.Label(select_frame_3, bg = "green", text = "{} range\n {} to {}".format(column,dataframe[column].min(), dataframe[column].max()))
        d["title"].place(relwidth = 1/3, relheight = 1/20, relx = 0, rely = place/20)
        x[column] = d
        #print(len(x))
    
    elif dataframe[column].dtype == "bool":
        d = dict()
        d["B"] = tk.Button(select_frame_3, bg = "white", text = "Include All")
        d["B"].config(command = lambda:boolchange(d["B"]))
        d["B"].place(relwidth = 1/3, relheight = 1/20, relx = 1/3, rely = place/20)
        d["title"] = tk.Label(select_frame_3, text = column, bg = "green")
        d["title"].place(relwidth = 1/3, relheight = 1/20, relx = 0, rely = place/20)
        x[column] = d
        print("added bool:{}".format(column))

def boolchange(button):
    if button["bg"] == "white":
        button.config(text = "Only False", bg = "red")

    elif button["bg"] == "red":
        button.config(text = "Only True", bg = "yellow")

    elif button["bg"] == "yellow":
        button.config(text = "Include All", bg = "white")
        

def removeranges(column):
    try:
        for m in x[column].values():
            m.destroy()
        del x[column]
        #print(len(dfranges))
        #print(dfranges)
    except:
        pass;


############################################################
#Dataframe Button Functions
############################################################
def selectall(dataframe):
    if not toggledbuttons:
        for i in range(len(columnbutton)):
            columntoggle(columnbutton[i], dataframe)
    else:
        for i in range(len(toggledbuttons)):
            toggledbuttons[i]["bg"] = "purple";
        toggledbuttons.clear()
        deleteallranges()
        Prompt.config(text = "{} columns selected ".format(len(toggledbuttons)))

def addcolumnbuttons(dataframe):#Add column buttons is also loading of new dataframe
    deletebuttons(plotbuttons)
    deletebuttons(df_buttons)
    add_df_buttons(dataframe)
    add_plot_buttons(dataframe)
    deletebuttons(toggledbuttons)
    rownum = 0
    tempframe.place(relwidth = 0.45, relheight = 0.2, relx = 0.05, rely = 0.05)
    frame_1.place(relwidth = 0.45, relheight = 0.2, relx = 0.5, rely = 0.05)
    for index,column in enumerate(dataframe):
        rownum = rownum + 1
        if index % 6 == 0: 
            rownum = 0
        addcolumn(column,index, rownum, dataframe)
        

def addcolumn(column, index, rownum, dataframe):
    columnnum = math.floor(1 + index/6)
    columnbutton.append(tk.Button(tempframe, text = column, bg = "purple"))
    columnbutton[index].config(command = lambda:[columntoggle(columnbutton[index],dataframe)])
    columnbutton[index].grid(row = rownum, column = columnnum) 

def columntoggle(button, dataframe):
    if button["bg"] == "purple":
        button.config(bg = "red")
        toggledbuttons.append(button)
        makerange(dataframe,button["text"])
        Prompt.config(text = "{} columns selected ".format(len(toggledbuttons)))

    elif button["bg"] == "red":
        button.config(bg = "purple")
        toggledbuttons.remove(button)
        removeranges(button["text"])
        Prompt.config(text = "{} columns selected ".format(len(toggledbuttons)))


def add_df_buttons(dataframe):
    if not frame_1.grid_slaves():
        rownum = 0
        columnnum = 0
        df_buttons.append(tk.Button(frame_1, bg = "orange", text = "Select All", command = lambda:selectall(dataframe)))
        df_buttons.append(tk.Button(frame_1, bg = "orange", text = "Show Data", command = lambda:showdata(returnquery(dataframe))))
        df_buttons.append(tk.Button(frame_1, bg = "orange", text = "Shape", command = lambda:shape(returnquery(dataframe))))
        df_buttons.append(tk.Button(frame_1, bg = "orange", text = "Info", command = lambda:returnquery(dataframe).info()))
        #df_buttons.append(tk.Button(frame_1, bg = "orange", text = "Sum", command = lambda:Sum(returnquery(dataframe),Sumentry())))
        
        for x in range(len(df_buttons)):
            columnnum = columnnum+1
            df_buttons[x].grid(row = 0, column = columnnum)
    else:
        pass;


def add_plot_buttons(dataframe):
    if not plotbuttons:
        plotbuttons.append(tk.Button(frame_1, bg = "brown", text = "x = []".format(), command = lambda:selectall(dataframe)))
        plotbuttons.append(tk.Button(frame_1, bg = "brown", text = "y = []".format(), command = lambda:showdata(returnquery(dataframe))))
        plotbuttons.append(tk.Button(frame_1, bg = "brown", text = "Plot []".format(), command = lambda:shape(returnquery(dataframe))))
        plotbuttons.append(tk.Button(frame_1, bg = "brown", text = "Make Plot", command = lambda:returnquery(dataframe).info()))
        plotbuttons.append(tk.Button(frame_1, bg = "brown", text = "y2/by category(hue)".format(), command = lambda:showdata(returnquery(dataframe))))
        columnnum = 0

        for x in range(4):
            
            columnnum = columnnum+1
            plotbuttons[x].grid(row = 1, column = columnnum)
            
        plotbuttons[4].grid(row = 2, column = 2)

        plotbuttons[0].config(command = lambda:togglexy(plotbuttons[0]))
        plotbuttons[1].config(command = lambda:togglexy(plotbuttons[1]))
        plotbuttons[4].config(command = lambda:togglexy(plotbuttons[4]))
        plotbuttons[2].config(command = lambda:toggleplot(plotbuttons[2]))
        plotbuttons[3].config(command = lambda:Plot(plotbuttons[0]["text"], plotbuttons[1]["text"],plotbuttons[4]["text"] ,Plotoptions[plotbuttonstate], returnquery(dataframe)))
    else:
        pass;

def togglexy(xybutton):
    global xybuttonstate
    xybuttonstate = xybuttonstate + 1
    if xybuttonstate >= len(toggledbuttons):
        xybuttonstate = -1
        xybutton["text"] = "none"

    else:
        xybutton["text"] = toggledbuttons[xybuttonstate]["text"]
    
        

def toggleplot(Plotbutton):
    global plotbuttonstate
    plotbuttonstate = plotbuttonstate + 1
    if plotbuttonstate >= len(Plotoptions):
        plotbuttonstate = -1
        Plotbutton["text"] = "none"
    else:
        Plotbutton["text"] = Plotoptions[plotbuttonstate]
    
    

def Plot(x,y,y2,plot,dataframe):

    if plot == "Simpplot":
        if y2 == "y2/by category(hue)" or y2 == "none":
            X = dataframe.sort_values(x)[x]
            Y = dataframe.sort_values(y)[y]
            plt.title("{} by {}".format(x,y))
            plt.plot(X,Y)
            plt.xlabel(x)
            plt.ylabel(y)
            plt.show()
        else:
            X = dataframe.sort_values(x)[x]
            Y = dataframe.sort_values(y)[y]
            Y2 = dataframe.sort_values(y2)[y2]
            plt.title("{} and {} by {}".format(y,y2,x))
            plt.plot(X,Y, 's--b')
            plt.plot(X,Y2, 'o--r')
            plt.xlabel(x)
            plt.ylabel("{} and {}".format(y,y2))
            plt.legend([y,y2])
            plt.show()
    
    elif plot == "Scatter":
        if y2 == "y2/by category(hue)" or y2 == "none":
            X = dataframe.sort_values(x)[x]
            Y = dataframe.sort_values(y)[y]
            plt.title("{} by {}".format(x,y))
            plt.scatter(X,Y)
            plt.xlabel(x)
            plt.ylabel(y)
            plt.show()
        else:
            X = dataframe.sort_values(x)[x]
            Y = dataframe.sort_values(y)[y]
            Y2 = dataframe.sort_values(y2)[y2]
            plt.title("{} by {}, categorised by {} ".format(y,x,y2))
            plt.scatter(X,Y)
            plt.xlabel(x)
            plt.ylabel("{}".format(y))
            plt.show()

        pass;

    elif plot == "ScatterPlot":
        if y2 == "y2/by category(hue)" or y2 == "none":
            X = dataframe.sort_values(x)[x]
            Y = dataframe.sort_values(y)[y]
            plt.title("{} by {}".format(x,y))
            sns.scatterplot(X,Y)
            plt.xlabel(x)
            plt.ylabel(y)
            plt.show()
        else:
            X = dataframe.sort_values(x)[x]
            Y = dataframe.sort_values(y)[y]
            Y2 = dataframe.sort_values(y2)[y2]
            plt.title("{} by {}, categorised by {} ".format(y,x,y2))
            sns.scatterplot(X,Y,hue=Y2)
            plt.xlabel(x)
            plt.ylabel("{}".format(y))
            plt.show()

        pass;

    elif plot == "Bar":
        if y2 == "y2/by category(hue)" or y2 == "none":
            X = dataframe.sort_values(x)[x]
            Y = dataframe.sort_values(y)[y]
            plt.title("{} by {}".format(x,y))
            plt.bar(X,Y)
            plt.xlabel(x)
            plt.ylabel(y)
            plt.show()
        else:
            X = dataframe.sort_values(x)[x]
            Y = dataframe.sort_values(y)[y]
            Y2 = dataframe.sort_values(y2)[y2]
            plt.title("{} and {}, by {} ".format(y,y2,x))
            plt.bar(X,Y2)
            plt.bar(X,Y, bottom=Y2)
            plt.xlabel(x)
            plt.legend([y,y2])
            plt.show()

    elif plot == "BarPlot":

        if y2 == "y2/by category(hue)" or y2 == "none":
            plt.title("{} by {}".format(x,y))
            sns.barplot(x,y,data=dataframe)
            plt.show()

        else:
            plt.title("{} by {}".format(x,y))
            sns.barplot(x,y,data=dataframe, hue=y2)
            plt.show()

    elif plot == "Histogram":
        legend = []
        if y2 != "y2/by category(hue)" and  y2 != "none":
            Y2 = dataframe.sort_values(y2)[y2]
            plt.hist(Y2, alpha = 0.5)
            legend.append(y2)

        if x != "x = []" and  x != "none":
            X = dataframe.sort_values(x)[x]
            plt.hist(X, alpha = 0.5)
            legend.append(x)

        if y != "y = []" and  y != "none":
            Y = dataframe.sort_values(y)[y]
            plt.hist(Y, alpha = 0.5)
            legend.append(y)
        plt.legend(legend)
        plt.show()
        pass;
    
############################################################
#Utility functions
############################################################


def increase_File_count():
    global File_count;
    File_count =+ 1;

def check_directory(Owner,Filerequest, checkmode):
    thispath = InitialPath+Owner+"\\"+Filerequest

    if checkmode == 0 or checkmode == "Initial":

        if not os.path.exists(InitialPath):
            os.mkdir(InitialPath);
            print("Created initial path in {}".format(InitialPath))
            return "Init New";
        else:
            print("Initial Path already exists in {} ".format(InitialPath))
            return "Init old"

    elif checkmode == 1 or checkmode =="New Request":
        if os.path.exists(thispath):
            print("These files already exist in {} , or initial path just created ".format(thispath))
            return "Old";

        elif not os.path.exists(InitialPath+Owner):
            os.mkdir(InitialPath+Owner)
            print("Created folder for dataset owner {} ".format(Owner))
            return "New";
        else:
            return "New"

    # Lower case owner must be separate from uppercase owner
    elif checkmode == 2 or checkmode =="All Existing" :

        if not len(os.listdir(InitialPath)) < 1:
            stats = []
            for owner in os.listdir(InitialPath):
                Folders = dict()
                
                for folder in os.listdir(InitialPath+owner):
                    Files = os.listdir(InitialPath+owner+"\\"+folder);
                    NewFiles = dict()
                    for File in Files:
                        NewFiles[File] = pd.read_csv(InitialPath+owner+"\\"+folder+"\\"+File)
                        increase_File_count();
                        
                    Folders[folder] = NewFiles;
                    #print("Files \t{}\t in Folder {}".format(NewFiles.keys(), folder))
                owners[owner] = Folders
                #print("Owner {} has folders {}".format(owner, owners[owner].keys()))
                
            #print("owner \t{}".format(owners.keys()))

            return os.listdir(InitialPath)
        else:
            return "No Files"

def close_window(root, buttonlist):
    deletebuttons(buttonlist)
    root.destroy();


def NewReqest(Owner, Filerequest):
    check_directory("","",0)
    
    if check_directory(Owner,Filerequest, 1) == "New" and Owner != "":
        try:
            kaggle.api.dataset_download_files(Owner+"/"+Filerequest,path=InitialPath+Owner+"\\"+Filerequest, quiet= False, unzip=True, force=False);
            
            
            check_directory("","",2)
            deletebuttons(owneruibuttons)
            deletebuttons(folderuibuttons)
            Prompt.config(text = "Download completed")
        except:
            if len(os.listdir(InitialPath+Owner)) < 1:
                os.rmdir(InitialPath+Owner)
            else:
                pass;
            print("File does not exist or formating incorrect, removed directory")
            Prompt.config(text = "File does not exist or formating incorrect.")
    elif Owner == "" or Filerequest == "":
        Prompt.config(text = "Input fields are empty")

    else:
        Prompt.config("{} by {} already exists in stored database".format(Filerequest,Owner))
        pass;



############################################################
#UI calling functions
############################################################

def foldersui(Owner):    
    deletebuttons(folderuibuttons)
    for index, folder in enumerate(os.listdir(InitialPath+Owner)):
        addfolderbuttons(index, folder, owner=Owner)
        #print("finished foldersui")      

def ownersui():
    ownerlist = check_directory("","",2)
    for index, df_dict in enumerate(owners.values()):
        for foldername in df_dict:
            addownerbuttons(index, ownerlist=ownerlist);
            #print("{} is {}".format(index,owneruibuttons[index]["text"]))
    print("finished ownersui")






############################################################
#UI Functions
############################################################
def start():
    check_directory("","",0)
    ownersui();
    select_root.mainloop()

def select_gui():
    ownersui()
    Title.config(text = "Bongs data analyser")
    Add_File_button.place(relwidth = 1/5, relheight = 1/5, relx = 2/5, rely = 4/5)
    
    Ownerentrylabel.place(relwidth = 3/9, relheight = 2/9, relx = 1/9, rely = 1/9)
    
    Ownerentry.place(relwidth = 3/9, relheight = 1/3, relx = 1/9, rely = 1/3)

    
    Datalabel.place(relwidth = 3/9, relheight = 2/9, relx = 5/9, rely = 1/9)
    
    Dataentry.place(relwidth = 3/9, relheight = 1/3, relx = 5/9, rely = 1/3)
    

    close.config(text = "exit", command = lambda:[close_window(select_root, fileuibuttons)]);
    
    
    Prompt.config(text = "")

def df_ui(WIDTH,HEIGHT, owner, folder):
    deletebuttons(folderuibuttons)
    deletebuttons(owneruibuttons)
    Add_File_button.place_forget()
    Ownerentrylabel.place_forget()
    Ownerentry.place_forget();
    Dataentry.place_forget();
    Datalabel.place_forget();

    Title.config(text = "{} - {}".format(owner,folder))

    for index, File in enumerate(owners[owner][folder]):
        addfilebuttons(owner, folder, File, index)

        

    close.config(text = "back", command = lambda:[backbutton()]);
    Prompt.config(text = "Select dataset")
    ownerlist = check_directory("","",2)

############################################################
#General Button Functions
############################################################
    

def addownerbuttons(num, ownerlist):
    yplace = 1+(num)
    owneruibuttons.append(tk.Button(select_frame_2))
    owneruibuttons[num].config(command=lambda:[foldersui(owneruibuttons[num]["text"])], text = ownerlist[num])
    owneruibuttons[num].place(relwidth = 5/9, relheight = 1/15, relx = 2/9, rely = yplace/15)

def addfolderbuttons(num, folder, owner):
    yplace = 1+(num)
    folderuibuttons.append(tk.Button(select_frame_3))
    folderuibuttons[num].config(text = folder, bg = "gray", command = lambda:[df_ui(800, 800, owner, folder)])
    folderuibuttons[num].place(relwidth = 5/9, relheight = 1/15, relx = 2/9, rely = yplace/15) 

def addfilebuttons(owner,folder, File, index):
    yplace = 1+index
    df = owners[owner][folder][File]
    fileuibuttons.append(tk.Button(text = File, master=select_frame_2))
    fileuibuttons[index].config(command = lambda:[deleteallranges(),deletebuttons(columnbutton),deletebuttons(plotbuttons),addcolumnbuttons(df), Prompt.config(text = "Select columns on left.")])
    fileuibuttons[index].place(relwidth = 5/9, relheight = 1/15, relx = 2/9, rely = yplace/15)
    
def deletebuttons(buttonlist):
    for button in buttonlist:
        button.destroy();
    buttonlist.clear();

def deleteallranges():
    try:
        for column in x.keys():
            for m in x[column].values():
                m.destroy()
        x.clear()
    except:
        pass;

def backbutton():
    deletebuttons(fileuibuttons)
    deletebuttons(columnbutton)
    deletebuttons(df_buttons)
    deletebuttons(plotbuttons)
    deleteallranges()
    tempframe.place_forget()
    frame_1.place(relwidth = 0.9, relheight = 0.2, relx = 0.05, rely = 0.05),
    select_gui()
############################################################
#Start
############################################################

start();
