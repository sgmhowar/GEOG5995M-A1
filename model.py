#%%  PREPARATION  %%#
#%% Import Packages
import agentframework as af #Contains Wolf and Sheep Classes and several of the functions to model them
import csv #Needed to import environment
import random #Randomises movement order of agents to reduce model artifacting
import matplotlib #Plotting
import tkinter as tk #Creating GUI
matplotlib.use('TkAgg') 
import matplotlib.pyplot #Plotting
import matplotlib.animation #Plotting as animation

        
#%% Variable and List Creation

# Set Variables
MaxBound = 299 # Maximum extent of environment (Ensure this doesn't exceed boundaries of enviroment file (i.e. do not increase beyond 299 or decrease below 0))
MinBound = 0 # Minimum extent of environment (Ensure this doesn't exceed boundaries of enviroment file (i.e. do not increase beyond 299 or decrease below 0))
neighbourhood = 20 # Distance sheep can share over
num_of_agents = 10 # Number of Sheep
pack_size = 2 # Number of Wolves
wolfspeed = 5 # Speed Wolves move at
runs = 100 # Max number of model iterations

# Create Lists - empty lists for appending agents to
agents = [] # List for Sheep Agents
environment = [] # List for Environment Data
wolves = [] # List for Wolf Agents

# Figure formatting
fig = matplotlib.pyplot.figure(figsize=(7, 7)) # Create blank figure for plotting on
ax = fig.add_axes([0, 0, 1, 1]) # Added axis to figure

#%% Reading in the Environment from a text file

environment.clear() # Empty Environment (blank slate)
f = open('ENV', newline='') # Loads text file into model
ENV = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC) # Read text file as a CSV file
for rows in ENV: # For each row in the CSV file:
    values = []   #Create a list to store this rows scores
    environment.append(values) #add this row to main environment list
    for pv in rows: # for each pixel value:
        values.append(pv) #Add pixel value to row
f.close() 

#delete values used for reading to clean up:
del pv
del rows
del values
#%% Create Agents and Wolves

agents.clear() #ensure blank slate for sheep agent creation
wolves.clear() #ensure blank slate for wolf agent creation

for i in range(num_of_agents): #For every desired sheep
    agents.append(af.Agent(environment, agents)) # Create sheep agent and generate start coordinatees
    
for j in range(pack_size): #For every Desired Wolf
    wolves.append(af.Wolf(environment,agents)) # Create Wolf agent and generate start coordinatees

#%% Kill Function - Not included in agentframework to simplify editing number of sheep

def kill(self, agents):
    global num_of_agents # Allows function to edit the sheep number globally (prevents indices error when a sheep has been killed)
    for agent in self.prey: #For every sheep
        if agent.x == self.x and agent.y == self.y: # If this sheep shares a space with the wolf
            agents.remove(agent) # remove sheep from sheep list
            num_of_agents -=  1 # reduce sheep count by one
            print("Sheep Eaten!") # notification of successful kill
            if num_of_agents == 0:
                print ("All sheep eaten!!!")
            
#%% Complete Simulation Function

def sim(self):
    fig.clear()  # ensure blank slate for figure

    for j in random.sample(range(num_of_agents), num_of_agents): # for every sheep agent (random order to reduce model artifacting)
        af.eat(agents[j]) #perform eat function
        af.move(agents[j], MinBound, MaxBound) # move agent within constratints of the model
        af.share(agents[j], neighbourhood) #share food with other sheep in designiated radius
    for j in random.sample(range(pack_size), pack_size): # for every wolf agent (random order to reduce model artifacting)
        af.hunt(wolves[j], wolfspeed, MaxBound, num_of_agents) # Makes Wolves chase down the sheep
        kill(wolves[j], agents) # Removes sheep if wolf has ccaught it (see above code chunk)

    for k in range(num_of_agents): #For every sheep
        for z in range(pack_size): #And every wolf
            matplotlib.pyplot.ylim(MinBound, MaxBound) #limit y axis to environment
            matplotlib.pyplot.xlim(MinBound, MaxBound) #limit x axis to environment
            matplotlib.pyplot.imshow(environment, alpha=0.8) #plot environment
            matplotlib.pyplot.scatter(agents[k].x,agents[k].y, color = "white") #plot the sheep
            matplotlib.pyplot.scatter(wolves[z].x, wolves[z].y, color = "red") #plot the wolf

#%% Function for Model Loop - limits model to either iterations equal to runs variable or to when all sheep are eaten
def gen_function(runs):
    a = runs # a is set to begin at desired number of iterations
    living = True # sheep start off alive
    while a > 0 and living == True:
        yield a			
        a -= 1 # Each iteration drops 'a' by one, model ends when it hits zero
        if num_of_agents == 0: #i.e. due to wolves eating all sheep
            living == False # all sheep are dead so model ends

#%% GUI Functions

def run(): #Function for generating animation
   animation = matplotlib.animation.FuncAnimation(fig, sim, frames=gen_function(runs), repeat=False)
   canvas.draw()
        
def Stop(): # function for stopping the model at it's defined conclusion
    global root
    root.quit()
    print('Model Completed!')
    
def terminate():  # Function to force quit model
    global root
    root.quit()
    root.destroy()
       
#%% Run GUI
root = tk.Tk()    
root.wm_title("Model") #Set title

#Create canvas for drawing model onto
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Create buttons which can call functions. Here I have created a 'run' button
# and a 'stop' button
run_button = tk.Button(root, text="Run Model", command=run) #button to start model
quit_button = tk.Button(root, text="Stop Model", command=terminate) #button to stop model
run_button.configure(bg='green') #colours start button green
quit_button.configure(bg='red') #colours stop button red
run_button.pack(side=tk.BOTTOM) #locates start button at bottom of gui
quit_button.pack(side=tk.BOTTOM) #locates stop button at bottom of gui

tk.mainloop() #load up GUI
