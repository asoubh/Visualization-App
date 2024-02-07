import tkinter as tk
from tkinter.messagebox import showinfo

# module used to correcly change button bg color
import tkmacosx as MacTk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from backend import data_functs

# ===================================================================

##### -=-=-=- Primary GUI Functions -=-=-=- #####

global plt_count
plt_count=0

global Region
Region=None

global state_data_df
state_data_df=None

def plot_graph():
    global plt_count

    # clear plot
    if plt_count==1 or plt_count==3:
        # Clear existing plot, if any
        plt.clf()
        # Embed the cleared plot in the Tkinter window
        canvas.draw()

        print(plt_count)
        plt_count+=1

    # draw plot
    else:
        # Clear existing plot, if any
        plt.clf()

        # Plot the graph y=x
        x = np.linspace(-10, 10, 100)
        y = x

        plt.plot(x, y, label="y=x", marker='o')
        plt.title("Graph of y=x")
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.legend()

        # Embed the plot in the Tkinter window
        canvas.draw()

        print(plt_count)
        plt_count+=1


##### Select region of interest for analysis
# passing event initiates action on event bound to box
def region_selected(event):
    print('first box clicked')

    global Region
    Region = usr_region_lstbx.get(usr_region_lstbx.curselection())

    # if the user selects 'National' for the region
    if Region == 'National':
        print('National select')
        
        # pull data for country
        national_data_df, l1_params = data_functs.get_national_data()
        #@@@@ STORE DF IN GLOBAL VARIABLE TO BE REFERENCED LATER
    
    # if the user selects 'State' for the region
    elif Region == 'State':
        print('State select')

        # Call here - STORE DF IN GLOBAL VARIABLE TO BE REFERENCED LATER
        global state_data_df

        # pull data for country
        # metadata "meta" field filtered out
        state_data_df, l1_params = data_functs.get_state_data('WA')

    # populate level 1 list box
    # clear ALL listbox data
    l1_param_lstbx.delete(0, tk.END)

    #@@@@ CLEAR ALL LOWER LEVEL LISTBOXES & Plot
    l2_param_lstbx.delete(0, tk.END)

    for metric in l1_params:
        # capitalize the word
        metric=metric.capitalize()

        # insert items into listbox
        l1_param_lstbx.insert(tk.END, metric)

# passing event initiates action on event bound to box
def L1_lstbx_sel(event):
    print('second box clicked')
    print('Level 1 listbox selection: {}'.format(l1_param_lstbx.get(l1_param_lstbx.curselection())))

    # call region that was selected
    global Region

    # if the user selects 'National' for the region
    #@@@@ implement for national data as well
    if Region == 'National':
        print('nation selection, still need to implement')

        l2_params=['no', 'entries']

    # if the user selects 'State' for the region
    elif Region == 'State':
        # call for input to get L2 params
        global state_data_df

        # get L2 params based on L1 input
        # @@@ add region as argument
        l2_params = data_functs.get_L2_params(state_data_df, l1_param_lstbx.get(l1_param_lstbx.curselection()))

        print('STATE - Level 2 params: {}'.format(l2_params))

    # populate level 2 list box
    # clear ALL listbox data
    l2_param_lstbx.delete(0, tk.END)

    #@@@@ CLEAR ALL LOWER LEVEL LISTBOXES & Plot
    # l3, l4, l5 params 

    for metric in l2_params:
        # capitalize the word
        metric=metric.capitalize()

        # insert items into listbox
        l2_param_lstbx.insert(tk.END, metric)

##### -=-=-=- Main GUI Framework -=-=-=- #####
# colors for main GUI
main_bg='#da2a3e' # deep red
main_btns='#c96965' # mild pink

# listbox predefined width
lstbx_width=10

main_window = tk.Tk()
main_window.title("Covid Analysis App")
main_window.geometry('1000x1000')
main_window.config(bg=main_bg)


### LISTBOX 1 - Region Selection ###
# list analysis type to be chosen
region_list = ('National', 'State')

# make analysis type a tkinter variable
tk_region_list = tk.Variable(value=region_list)

# create listbox
usr_region_lstbx = tk.Listbox(main_window,
                                listvariable=tk_region_list,
                                height=6,
                                width=lstbx_width,
                                selectmode=tk.SINGLE)
usr_region_lstbx.place(x=100, y=100)

# bind click event to list box
usr_region_lstbx.bind("<ButtonRelease-1>", region_selected)

### LISTBOX 2 - Level 1 parameter selection ###
# list analysis type to be chosen
l1_metric_lst = []

# make analysis type a tkinter variable
tk_l1_metric_lst = tk.Variable(value=l1_metric_lst)

# create listbox
l1_param_lstbx = tk.Listbox(main_window,
                                listvariable=tk_l1_metric_lst,
                                height=6,
                                width=lstbx_width,
                                selectmode=tk.SINGLE)
l1_param_lstbx.place(x=300, y=100)

# bind click event to list box
l1_param_lstbx.bind("<ButtonRelease-1>", L1_lstbx_sel)

### LISTBOX 3 - Level 2 parameter selection ###
# list analysis type to be chosen
l2_metric_lst = []

# make analysis type a tkinter variable
tk_l2_metric_lst = tk.Variable(value=l2_metric_lst)

# create listbox
l2_param_lstbx = tk.Listbox(main_window,
                                listvariable=tk_l2_metric_lst,
                                height=6,
                                width=lstbx_width,
                                selectmode=tk.SINGLE)
l2_param_lstbx.place(x=500, y=100)

# bind click event to list box
l2_param_lstbx.bind("<ButtonRelease-1>", None)

########################## GRAPHING

#Create a button to plot the graph
plot_button = tk.Button(main_window, text="Plot Graph", command=plot_graph)
plot_button.place(x=100, y=350)

# Create a Matplotlib figure and embed it in the Tkinter window
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=main_window)
canvas_widget = canvas.get_tk_widget()
canvas_widget.place(x=300, y=300)


# execute application in mainloop
main_window.mainloop()