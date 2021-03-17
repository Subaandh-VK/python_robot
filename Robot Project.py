#!/usr/bin/env python
# coding: utf-8

# # Robot Project
# 
# #### Run all cells before running the main function.
# #### Teleportation is activated after 80 moves.
# #### Auto-Play performs 50 moves after next operation should be selected.
# #### Red and Blue robots cannot attack neutral robots wherea neutral robots can.
# #### After changing values press Submit&Start to configure the values.

# # Game Board Class

# In[1]:


class GameBoard():
    def __init__(self, robots,size=6, redbots=6,bluebots=6, toss = 0, moves = 0):
        self.robots = robots
        self.size = size
        self.redbots = redbots
        self.bluebots = bluebots
        self.toss = toss
        self.moves = moves

    def select_robot(self, color):
        while True:
            i = random.randint(0, self.size - 1)
            j = random.randint(0, self.size - 1)
            
            robot = self.robots[i][j];
            
            if (robot.value['bg'] == color):
                robot.move(robot, color, i, j)
                break
        
    def select_team(self):
        #for the next turn the other team will play so change toss value
        if (self.toss == 1):
            self.toss = 2
            return "blue"
        else:
            self.toss = 1
            return "red"
    
    def show_moves(self):
            label = Label(interface, text = "Moves")
            label.grid(row = 0, column = self.size + 1)
            label = Label(interface, text = str(self.moves), bg = "green")
            label.grid(row = 0, column = self.size + 2)
            interface.update()

    def play(self):
        team = self.select_team()
        self.select_robot(team)
        if (self.moves >= 80 and self.moves % 2 == 0):
            self.move_neutral_robot()

        self.show_moves()
        interface.update()
        self.check_winner()

    def auto_play(self):
        self.display_message("Clicked Auto-Play. Automatically playing next 50 Turns")
        time.sleep(3)
        interface.update()
        turns = 50
        while(self.bluebots != 0 and self.redbots != 0 and turns > 0):
            team = self.select_team()
            self.select_robot(team)
            if (self.moves >= 80 and self.moves % 2 == 0):
                self.move_neutral_robot()
            
            self.show_moves()
            interface.update()
            time.sleep(0.5)
            turns -= 1

        self.check_winner()
        
    
    def display_message(self, message, color= "black"):
            label = Label(interface, text = message, bg = "white", fg = color, width = 50)
            label.grid(row = 0, column = self.size + 3)
            interface.update()

    def check_winner(self):
        label = None

        if (self.bluebots == 0):
            self.display_message("RED Team Wins Congratulations!", "green")
            manual["state"] = "disabled"
            auto["state"] = "disabled"

        if (self.redbots == 0):
            self.display_message("BLUE Team Wins Congratulations!", "green")
            manual["state"] = "disabled"
            auto["state"] = "disabled"

    def is_attackable(self, atk, opp):
        if (atk.value['bg'] == opp.value['bg']):
            return False

        if (opp.active != 1):
            return False

        return True
    
    def move_neutral_robot(self):
        for i in range(self.size):
            for j in range(self.size):
                robot = self.robots[i][j]

                if (robot.active == 3):
                    robot.move(robot, "green", i, j)
                    break

    def teleport(self):
        mvt_list = ["up", "down", "left", "right"]
        facing_list = ["↑", "↓", "←", "→" ]
        
        for i in range(self.size):
            for j in range(self.size):
                robot = self.robots[i][j]
                
                # If we find an deactive robot we make it a neutral robot
                if (robot.active == 2):
                    robot.value.itemconfig(robot.text, text= facing_list[random.randint(0,3)])
                    robot.value.configure(bg='green')
                    robot.direction = mvt_list[random.randint(0,3)]
                    robot.active = 3
                    time.sleep(2)
                    return


# # Robot Class

# In[2]:


class Robots():
    def __init__(self, body = None, weapon = None, text=None, activebody = None, activeweapon = None, 
                 value = None, direction = None, active = 0, behaviour = None, mvt = 1):
        self.body = body
        self.activebody = activebody
        self.weapon = weapon
        self.activeweapon  = activeweapon
        self.value = value
        self.text = text
        self.direction = direction
        self.active = active
        self.behaviour = behaviour
        self.mvt = mvt
    
    # Move the robots only to postion where there are no robots or neutral robots
    def check_empty(self, robot):
        return robot.active == 0 or robot.active == -1

    def move(self, robot, color, i, j):
        robots = game.robots
        movement_direction = facing_direction = found = 0
        robot_new_pos = None

        movement_direction = random.randint(0,3)
        facing_direction = random.randint(0,3)

        if (i == 0): #To make the robots move downwards if it's the blue robot's first turn
            movement_direction = 1
        elif (i == game.size - 1): # #To make the robots move upwards if it's the red robot's first turn
            movement_direction = 0

        mvt_list = ["up", "down", "left", "right"]
        facing_list = ["↑", "↓", "←", "→" ]

    
        if (mvt_list[movement_direction] == "up"):
            if (i-1 >= 0 and self.check_empty(robots[i-1][j])):
                robot_new_pos = robots[i-1][j]
                i = i - 1
                found = 1
        
        if (mvt_list[movement_direction] == "down" ):
            if (i+1 < game.size and self.check_empty(robots[i+1][j])):
                robot_new_pos = robots[i+1][j]
                i = i + 1
                found = 1
        
        if (mvt_list[movement_direction] == "left"):
            if (j-1 >= 0 and self.check_empty(robots[i][j-1])):
                robot_new_pos = robots[i][j-1]
                j = j - 1
                found = 1
        
        if (mvt_list[movement_direction] == "right"):
            if (j+1 < game.size and self.check_empty(robots[i][j+1])):
                robot_new_pos = robots[i][j+1]
                j = j + 1
                found = 1
        
        #If the robot moves in to a new position where there is a dead robot process the values in that position
        if (found == 1 and robot_new_pos.active == -1):
            game.display_message(color+ "bot @"+str(i)+" "+ str(j)+" Gaining 1 HP")
            #Increasing the HP by one as dead robots drop bodies and they are worth 1HP
            robot.activebody.body_HP += 1
            
        #Copy all values to the new position
        if (found == 1):
                robot_new_pos.value.itemconfig(robot.text, text= facing_list[facing_direction])
                robot_new_pos.value.configure(bg=color)
                robot_new_pos.weapon = robot.weapon
                robot_new_pos.activeweapon = robot.activeweapon
                robot_new_pos.body = robot.body
                robot_new_pos.activebody = robot.activebody
                robot_new_pos.direction = mvt_list[facing_direction]
                robot_new_pos.active = robot.active
                
                # Deactivate the existing robot's index 
                robot.value.configure(bg='white')
                robot.value.itemconfig(robot.text, text= '')
                robot.direction = None
                robot.active = 0
        
        #The robot has move now we should perform the attack
        if (robot_new_pos == None):
            robot_new_pos = robot
            
        # The turn has ended so changing the robot's weapon and body type
        robot_new_pos.choose_weapon()
        robot_new_pos.choose_body()
        
        robot_new_pos.activeweapon.attack(game.robots, i, j)
        
        game.moves += 1 # Counting moves to make teleportation and replace deactivated robots by neutral robots
        
        if (game.moves % 80 == 0):
            game.display_message("TELEPORTING: Deactivated to Neutral", "green")
            game.teleport()

    def choose_weapon(self):
        self.activeweapon = self.weapon[random.randint(0, len(self.weapon) -1)]
    def choose_body(self):
        self.activebody = self.body[random.randint(0, len(self.body) -1)]
    
    def deactivate(self):
        game.display_message("HP 0 - deactivating "+ self.value['bg']+ " robot")
        if (self.value['bg'] == "blue"):
            value = game.bluebots
            game.bluebots =  value - 1
        elif (self.value['bg'] == "red"):
            value = game.redbots
            game.redbots =  value - 1
            
        self.value.configure(bg="black")
        self.value.itemconfig(self.text, text = ' ')
        self.direction = "deactivated"
        self.active = -1;
        
        game.check_winner()

    def calculate_damage(self, damage):
        game.display_message("Attack Successful", "green")
        self.activebody.body_HP -= damage
        if (self.activebody.body_HP <= 0):
            self.deactivate()


# # Weapons class

# In[3]:


class Weapon():
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

class Basic(Weapon):
    def __init__(self):
        super().__init__("Basic", 1)

    def attack(self,robots, i, j):
        atk_robot = robots[i][j]
        opp_robot = game.robots
        
        for x in range(1,3):
            game.display_message("Basic Attack")
            # checking if its a valid index and performing attack if it's a active robot
            if (atk_robot.direction == "up" and i-x >= 0):
                if (game.is_attackable(atk_robot, opp_robot[i-x][j])):
                    opp_robot[i-x][j].calculate_damage(self.damage)
            
            if (atk_robot.direction == "down" and i+x < game.size):
                if (game.is_attackable(atk_robot, opp_robot[i+x][j])):
                    opp_robot[i+x][j].calculate_damage(self.damage)
                
            if (atk_robot.direction == "left" and j-x >= 0):
                if (game.is_attackable(atk_robot, opp_robot[i][j-x])):
                    opp_robot[i][j-x].calculate_damage(self.damage)
            
            if (atk_robot.direction == "right" and j+x < game.size):
                if (game.is_attackable(atk_robot, opp_robot[i][j+x])):
                    opp_robot[i][j+x].calculate_damage(self.damage)
        
class Laser(Weapon):
    def __init__(self):
        super().__init__("Laser", 1)
    
    def attack(self, robots, i, j):
        atk_robot = robots[i][j]
        opp_robot = game.robots
        
        game.display_message("Laser Attack")
        for x in range(0, game.size):
            if (atk_robot.direction == "up" and i-x >= 0):
                if (game.is_attackable(atk_robot, opp_robot[i-x][j])):
                    opp_robot[i-x][j].calculate_damage(self.damage)
            
            if (atk_robot.direction == "down" and i+x < game.size):
                if (game.is_attackable(atk_robot, opp_robot[i+x][j])):
                    opp_robot[i+x][j].calculate_damage(self.damage)
                
            if (atk_robot.direction == "left" and j-x >= 0):
                if (game.is_attackable(atk_robot, opp_robot[i][j-x])):
                    opp_robot[i][j-x].calculate_damage(self.damage)
            
            if (atk_robot.direction == "right" and j+x < game.size):
                if (game.is_attackable(atk_robot, opp_robot[i][j+x])):
                    opp_robot[i][j+x].calculate_damage(self.damage)


class Sword(Weapon):
    def __init__(self):
        super().__init__("Sword", 2)
    
    def attack(self, robots, i, j):
        atk_robot = robots[i][j]
        opp_robot = game.robots
        x = 1 #Because sword makes a slash only in the front and diagonals
        
        
        game.display_message("Sword Attack")
        if (atk_robot.direction == "up"):
            #Straight slash when robot is facing forward
            if (i-x >= 0):
                if (game.is_attackable(atk_robot, opp_robot[i-x][j])):
                    opp_robot[i-x][j].calculate_damage(self.damage)
            
            #Diagonal left slash when robot is facing forward
            if (i-x >= 0 and j-x >=0):
                if (game.is_attackable(atk_robot, opp_robot[i-x][j-x])):
                    opp_robot[i-x][j-x].calculate_damage(self.damage)
            
            #Diagonal right slash when robot is facing forward
            if (i-x >= 0 and j+x < game.size):
                if (game.is_attackable(atk_robot, opp_robot[i-x][j+x])):
                    opp_robot[i-x][j+x].calculate_damage(self.damage)
            
        if (atk_robot.direction == "down"):
            if (i+x < game.size):
                if (game.is_attackable(atk_robot, opp_robot[i+x][j])):
                    opp_robot[i+x][j].calculate_damage(self.damage)
                
            if (i+x < game.size and j-x >= 0):
                if (game.is_attackable(atk_robot, opp_robot[i+x][j-x])):
                    opp_robot[i+x][j-x].calculate_damage(self.damage)
            
            if (i+x < game.size and j+x < game.size):
                if (game.is_attackable(atk_robot, opp_robot[i+x][j+x])):
                    opp_robot[i+x][j+x].calculate_damage(self.damage)
            
        if (atk_robot.direction == "left"):
            if (j-x >= 0):
                if (game.is_attackable(atk_robot, opp_robot[i][j-x])):
                    opp_robot[i][j-x].calculate_damage(self.damage)
                
            if (j-x >= 0 and i-x >= 0):
                if (game.is_attackable(atk_robot, opp_robot[i-x][j-x])):
                    opp_robot[i-x][j-x].calculate_damage(self.damage)
                
            if (j+x < game.size and i-x >= 0):
                if (game.is_attackable(atk_robot, opp_robot[i-x][j+x])):
                    opp_robot[i-x][j+x].calculate_damage(self.damage)
            
            
        if (atk_robot.direction == "right"):
            if (j+x < game.size):
                if (game.is_attackable(atk_robot, opp_robot[i][j+x])):
                    opp_robot[i][j+x].calculate_damage(self.damage)
        
            if (j+x < game.size and i-x >= 0):
                if (game.is_attackable(atk_robot, opp_robot[i-x][j+x])):
                    opp_robot[i-x][j+x].calculate_damage(self.damage)
            
            if (j+x < game.size and i+x < game.size):
                if (game.is_attackable(atk_robot, opp_robot[i+x][j+x])):
                    opp_robot[i+x][j+x].calculate_damage(self.damage)

class Explosion(Weapon):
    def __init__(self):
        super().__init__("Explosion", 1)
        
    def attack(self, robots, i, j):
        atk_robot = robots[i][j]
        opp_robot = game.robots
        x = 1

        
        game.display_message("Explosion Attack")
        #Exlposion is common irrespective of the facing direction so all considering all neighbouring cells
        if (i-x >= 0 and j-x >=0):
            if (game.is_attackable(atk_robot, opp_robot[i-x][j-x])):
                opp_robot[i-x][j-x].calculate_damage(self.damage)
            
        if (i-x >= 0):
            if (game.is_attackable(atk_robot, opp_robot[i-x][j])):
                opp_robot[i-x][j].calculate_damage(self.damage)
            
        if (i-x >= 0 and j+x < game.size):
            if (game.is_attackable(atk_robot, opp_robot[i-x][j+x])):
                opp_robot[i-x][j+x].calculate_damage(self.damage)
            
        if (j-x >= 0):
            if (game.is_attackable(atk_robot, opp_robot[i][j-x])):
                opp_robot[i][j-x].calculate_damage(self.damage)
            
        if (j+x < game.size):
            if (game.is_attackable(atk_robot, opp_robot[i][j+x])):
                opp_robot[i][j+x].calculate_damage(self.damage)
                
        if (i+x < game.size and j-x >= 0):
            if (game.is_attackable(atk_robot, opp_robot[i+x][j-x])):
                opp_robot[i+x][j-x].calculate_damage(self.damage)
                
        if (i+x < game.size):
            if (game.is_attackable(atk_robot, opp_robot[i+x][j])):
                opp_robot[i+x][j].calculate_damage(self.damage)
            
        if (j+x < game.size and i+x < game.size):
            if (game.is_attackable(atk_robot, opp_robot[i+x][j+x])):
                opp_robot[i+x][j+x].calculate_damage(self.damage)

class Duallaser(Weapon):
    def __init__(self):
        super().__init__("Duallaser", 1)
    
    
    def attack(self, robots, i, j):
        atk_robot = robots[i][j]
        opp_robot = game.robots
        
        
        game.display_message("Dual laser Attack")
        for x in range(0, game.size):
            if (atk_robot.direction == "up" or atk_robot.direction == "down"):
                if (j-x >= 0 and game.is_attackable(atk_robot, opp_robot[i][j-x])):
                    opp_robot[i][j-x].calculate_damage(self.damage)
                if (j+x < game.size and game.is_attackable(atk_robot, opp_robot[i][j+x])):
                    opp_robot[i][j+x].calculate_damage(self.damage)
                
            if (atk_robot.direction == "left" or atk_robot.direction == "right"):
                if (i-x >= 0 and game.is_attackable(atk_robot, opp_robot[i-x][j])):
                    opp_robot[i-x][j].calculate_damage(self.damage)
                if (i+x < game.size and game.is_attackable(atk_robot, opp_robot[i+x][j])):
                    opp_robot[i+x][j].calculate_damage(self.damage)


# # Body Class

# In[4]:


class Body():
    def __init__(self, body_HP, body_mvt, body_slots):
        self.body_HP = body_HP
        self.body_mvt = body_mvt
        self.body_slots = body_slots
        
class Simple(Body):
    def __init__(self):
        super().__init__(2,0,1)

class Hard(Body):
    def __init__(self):
        super().__init__(5,0,1)
        
class Light(Body):
    def __init__(self):
        super().__init__(3,1,1)

class Battle(Body):
    def __init__(self):
        super().__init__(2,0,2)


# # Methods to create game, place robots, handle UI inputs

# In[5]:


def add_weapons(robot):
    robot.weapon = [Basic(), Laser(), Sword(), Explosion(), Duallaser()]
    robot.activeweapon = robot.weapon[0]
def add_bodies(robot):
    robot.body = [Simple(), Hard(), Light(), Battle()]
    robot.activebody = robot.body[0]

def place_robots(robots, size, redbots, bluebots, deactivebots):
    i = 0
    # First row so all robots face downwards
    for j in range(size):
        if (bluebots == 0):
            break
        robot = robots[i][j]
        robot.value.itemconfig(robot.text, text= '↓')
        robot.value.configure(bg='blue')
        robot.direction = "down"
        robot.active = 1
        add_bodies(robot)
        add_weapons(robot)
        bluebots -= 1

    i = size - 1
    # Last row so all robots face upwards
    for j in range(size):
        if (redbots == 0):
            break
        robot = robots[i][j]
        robot.value.configure(bg='red')
        robot.value.itemconfig(robot.text, text= '↑')
        robot.direction = "up"
        robot.active = 1
        add_bodies(robot)
        add_weapons(robot)
        redbots -= 1
    
    #Place deactivated robots in a random position except 1st row and last row
    while (deactivebots > 0):
        i = random.randint(1, size - 2) # row values from (1, size - 2) as we have blue bots in first row and the red bots in the last row
        j = random.randint(0, size - 1)
        
        robot = robots[i][j]
        if (robot.active == 1 or robot.active == 2):
            continue

        robot.value.configure(bg='grey')
        robot.value.itemconfig(robot.text, text= '')
        robot.direction = ""
        robot.active = 2
        add_bodies(robot)
        add_weapons(robot)
        deactivebots -= 1

def create_matrix(robots, size):
    multfactor = 6
    if (size > 10):
        multfactor = 5

    for i in range(size):
        for j in range(size):
            robots[i][j] = Robots()
            robots[i][j].value = Canvas(interface, bg='white', height = size*multfactor, width=size*multfactor)
            robots[i][j].text = robots[i][j].value.create_text(0, 0, text= '', fill = 'black',anchor=NW, font=("normal", size*4))
            robots[i][j].value.grid(row=i,column=j)

def create_game(size = 6, redbots = 6, bluebots = 6, deactivebots = 8):
    robots=[[0 for row in range(size)] for column in range(size)]
    displayrow = 1
    displaycolumn = size + 1
   
    create_matrix(robots, size)
    place_robots(robots, size, redbots, bluebots, deactivebots)

    # To Change board size
    sizel = Label(interface, text="Board Size",width = 12)
    sizel.grid(row = displayrow, column = displaycolumn)

    size_var = IntVar()
    size_var.set(size)
    boardsize = Spinbox(interface, from_=5, to=15, width = 5, textvariable=size_var)
    boardsize.grid(row = displayrow, column = displaycolumn+1)
    displayrow += 1

    # To Change red robots
    redl = Label(interface, text="Red bots:",width = 12)
    redl.grid(row = displayrow, column = displaycolumn)

    red_var = IntVar()
    red_var.set(redbots)
    red = Spinbox(interface, from_=1, to=size, width = 5, textvariable = red_var)
    red.grid(row = displayrow, column = displaycolumn+1)
    displayrow += 1

    # To Change blue robots
    bluel = Label(interface, text="Blue bots:", width = 12)
    bluel.grid(row = displayrow, column = displaycolumn)
    
    blue_var = IntVar()
    blue_var.set(bluebots)
    blue = Spinbox(interface, from_=1, to=size, width = 5, textvariable = blue_var)
    blue.grid(row = displayrow, column = displaycolumn+1)
    displayrow += 1
 
    # To Change deactive robots
    deactivel = Label(interface, text="Deactive bots:", width = 12)
    deactivel.grid(row = displayrow, column = displaycolumn)
    
    deact_var = IntVar()
    deact_var.set(deactivebots)
    deactive = Spinbox(interface, from_=0, to=size + 5, width = 5, textvariable=deact_var)
    deactive.grid(row = displayrow, column = displaycolumn+1)
    displayrow += 1

    # To Submit values and start new game
    create = Button(interface, text="Submit&Start", width = 12, command = lambda blue = blue, red = red, deactive = deactive, boardsize = boardsize:handle_start(blue, red, deactive, boardsize))
    create.grid(row = displayrow, column = displaycolumn)
    displayrow += 1
   
    global manual, auto
    manual = Button(interface, text = "Manual Play", width = 12, command = handle_manual)
    manual.grid(row = displayrow, column = displaycolumn)

    auto = Button(interface, text = "Auto Play", width = 12,command = handle_auto)
    auto.grid(row = displayrow, column = displaycolumn + 1)
    displayrow += 1

    stop = Button(interface, text = "Restart Game", width = 12, command = handle_restart)
    stop.grid(row = displayrow, column = displaycolumn)
    
    quit = Button(interface, text="Quit Game", width = 12, command = handle_quit)
    quit.grid(row = displayrow, column = displaycolumn + 1)
    displayrow += 1

    global game
    game = GameBoard(robots, size, redbots, bluebots);
    game.display_message("Welcome")


# # Button handlers

# In[6]:


def handle_start(blue, red, deactive, boardsize):
    size = int(boardsize.get())
    redbots = int(red.get())
    bluebots = int(blue.get())
    deactivebots = int(deactive.get())
    restart_game()
    create_game(size, redbots, bluebots, deactivebots)

def handle_quit():
    restart_game()
    interface.destroy()

def handle_auto():
    #if game is already started don't put toss
    if (game.toss == 0):
        game.toss = random.randint(1,2)
    game.auto_play()

def handle_manual():
    #if game is already started don't put toss
    if (game.toss == 0):
        game.toss = random.randint(1,2)
    game.play()

def handle_restart():
    restart_game()
    create_game()

def restart_game():
    for i in range(len(game.robots)):
        for j in range(len(game.robots)):
            game.robots[i][j] = 0

    for x in interface.winfo_children():
        x.destroy()


# # Main Function

# In[7]:


from tkinter import *
import tkinter as tk
import random
import time
import sys
import os

global interface
interface = tk.Tk()
interface.title("Robot Game")

create_game()

# create canvas
interface.mainloop()


# In[ ]:





# In[ ]:




