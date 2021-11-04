import random #used to generate random starting coordinates
import requests #Obtaining data from URL
import bs4 #formatting html data into usable format

#random.seed(999) # Optionally set seed for testing

#%% Web Scraping - used to set wolf start coordinates
r = requests.get('http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html') #import html data from url
content = r.text #format html content as string object
soup = bs4.BeautifulSoup(content, 'html.parser') #parses html data
td_ys = soup.find_all(attrs={"class" : "y"}) #isolate y values
td_xs = soup.find_all(attrs={"class" : "x"}) #isolate x values

#%% Objects

class Agent: #Used to create sheep
    def __init__(self, environment, others):
        self.environment = environment #stores environment data
        self.others = others #list of other sheep for interacting
        self.eaten = 0 #tracks volume eaten from environment
        self.x = random.randint(1,299) #random x coordinate
        self.y = random.randint(1,299) #random y coordinate
        
class Wolf: #used to create wolves
    def __init__(self, environment, prey):
        self.environment = environment #stores environment data
        self.prey = prey #list fo sheep for interacting (same data as Agent.others)
        self.x = int(td_xs[random.randint(1,100)].text) #random x coordinate from url file
        self.y = int(td_ys[random.randint(1,100)].text) #random y coordinate from url file
        
class tracking: #used for showing wolves the nearest sheeps coordinates
    def __init__(self, sx, sy, distance):
        self.distance = distance #stores distance of sheep from wolf
        self.sx = sx #stores x coordinate of said sheep
        self.sy = sy #stores said sheeps y coordinate
    
#%% Functions


def distance_between(firstagent, secondagent): #uses trigonometry to determine distance between two agents (used for sharing and hunting)
    return (((firstagent.x - secondagent.x)**2) + ((firstagent.y - secondagent.y)**2))**0.5


# Simulation functions

def eat(self): #Allows sheep to 'eat' data from underlying environment
    if self.environment[self.y][self.x] > 10: # If environment has a value of least 10
        self.environment[self.y][self.x] -= 10 #drop this value by 10
        self.eaten += 10 #increase amount sheep has 'eaten' by 10
    else: #if environment has a value less than 10
        self.eaten += self.environment[self.y][self.x] #amount sheep has 'eaten' increases by whatever value the environment has left
        self.environment[self.y][self.x] = 0 #environment value becomes 0
        
def move(self, minb, maxb): #function for sheep random movement
         if random.random() < 0.5 and self.y < maxb : #if random value (between 0 and 1) is less than 0.5 (so 50/50 chance) and moving wouldn't take the sheep out of the environment
             self.y += 1 #increase y coordinate by one
         else: #if random integer was greater than 0.5 (the other 50% chance) or the sheep was too close to the top boundary
             if self.y > minb: #so long as sheep isnt at the minimum boundary
                 self.y -=  1 #decrease y coordinate by one
         if random.random() < 0.5 and self.x < maxb: #repeats in exact same way but edits x coordinates using new random value independent of the one used for the y coordinates.
             self.x += 1
         else:
             if self.x > minb:
                 self.x -= 1

def share(self, neighbourhood): #function that allows sheep to share 'eaten' values with each other
    for agent in self.others: #performs check for every other sheep
        if agent != self: #ensures sheep doesn't share with itself (not that this would do anything)
            d = distance_between(self, agent) #measure distance between agents
            if d <= neighbourhood: #if other agent is within a sheeps sharing radius
                av = (self.eaten + agent.eaten) / 2 #calculate the average of their eaten stores
                self.eaten = av #set first agent's eaten volume to average
                agent.eaten = av #set other agent's eaten volume to average
                
def hunt(self, speed, MaxBoundary, targets): #function for wolves to hunt down sheep
    trace = [] # create a list for filling with tracking data
    closest = MaxBoundary #sets the base parameter for shortest distance to a sheep to max possible distance
    for agent in self.prey: #for every sheep
        trace.append(tracking(agent.x, agent.y, distance_between(self, agent))) #create an agent storing said sheeps coordinates and distance from wolf
    for t in range(targets): #for every sheep
        if trace[t].distance < closest: #if this sheep is closer than the previous closest sheep
            closest = trace[t].distance #set this as the shortest distance to a sheep
    for t in range(targets): #for every sheep
        if closest == trace[t].distance: #if this sheep is the closest
            if self.x + speed < trace[t].sx: #if full speed wont allow the wolf x coord to increase enough
                self.x += speed #increase x coordinate by max wolf movement
            else:
                if self.x - speed > trace[t].sx: #if full speed wont allow the wolf x coord to decrease enough
                    self.x -= speed #decrease x coordinate by wolf full speed
                else:
                    self.x = trace[t].sx #wolf must be within reach of sheep so move into sheep coordinates
        if closest == trace[t].distance: #repeats move conditions for y coordinates
            if self.y + speed < trace[t].sy:
                self.y += speed
            else:
                if self.y - speed > trace[t].sy:
                    self.y -= speed
                else:
                    self.y = trace[t].sy


            
            
    
                


        