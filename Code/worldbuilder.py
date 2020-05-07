# Import Python functions
import pygame
import pickle
from time import time
import math
import random

# Import our own functions
from classes.car_class import car
from classes.window_class import Window
from classes.world_class import World
from classes.game_class import car_game
import statespace
import motionplanning
import logResults



difficulty="Easy" #Easy, Medium, Hard, Extreme, Random
photoMode=False


needCheck=True
print("This is a building mode designed for picking the locations of the blue cars")
while needCheck:
    check=input("This mode will overwrite any previously saved blue car positions. Are you sure you want to continue? Type 'Yes' or 'No': ")
    if check.lower()=="no" or check.lower()=='n':
        print("Exiting")
        needCheck=False
        exit()
    elif check.lower()=="yes" or check.lower()=='y':
        needCheck=False
        print("Use the arrow keys to move the window, and then select where you'd like the blue cars to go")
        print("A blue car will appear where you have clicked, and it's location will be saved for later use")
        print("When you are done, hit Q to save and exit. The next time you run, change 'manuallyAddCars' to False in game.py and 'userDefinedCars' to True in the World class")
    else:
        print("I didn't understand. Please try again.")

bluecarlist=[]

print("Starting game")
game=car_game(difficulty) # Instantiate game

print("Generating world")
world=World(game,photoMode) # Generate world


# Run the game
while game.run:
    game.clock.tick(100)

    # # Update green cars
    # for active_car in game.active_list:
    #     active_car.spritex+=active_car.vel
    #     active_car.updateCarOrigin()

    # Get new events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.run = False

    keys = pygame.key.get_pressed()
    speed=10
    # Get cursor position for placing blue cars
    if keys[pygame.K_LEFT]:
        world.window.x-=speed
    elif keys[pygame.K_RIGHT]:
        world.window.x+=speed
    elif keys[pygame.K_UP]:
        world.window.y-=speed
    elif keys[pygame.K_DOWN]:
        world.window.y+=speed
    cursor=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    if click[0]==1:
        window_pos=(world.window.x,world.window.y)
        cursor_pos=(cursor[0]+window_pos[0],cursor[1]+window_pos[1])
        if world.window.top_shoulder_pos_y+world.window.y<=cursor_pos[1]<=world.window.lane_pos_y[0]+world.window.y:
            new_y=(world.window.top_shoulder_pos_y+world.window.lane_pos_y[0])/2+world.window.y

        if world.window.lane_pos_y[0]+world.window.y<=cursor_pos[1]<=world.window.lane_pos_y[1]+world.window.y:
            new_y=(world.window.lane_pos_y[0]+world.window.y+world.window.lane_pos_y[1]+world.window.y)/2
        
        if world.window.lane_pos_y[1]+world.window.y<=cursor_pos[1]<=world.window.lane_pos_y[2]+world.window.y:
            new_y=(world.window.lane_pos_y[1]+world.window.y+world.window.lane_pos_y[2]+world.window.y)/2

        if world.window.lane_pos_y[2]+world.window.y<=cursor_pos[1]<=world.window.bot_shoulder_pos_y+world.window.y:
            new_y=(world.window.lane_pos_y[2]+world.window.y+world.window.bot_shoulder_pos_y+world.window.y)/2

        new_obst=car(cursor_pos[0],new_y,"obstacle")
        game.obst_list.add(new_obst)
        game.all_sprites.add(new_obst)
        bluecarlist.append(cursor_pos)

    # world.updateWinPos(game)
    world.window.redrawGameWindow(game,world.WorldSize_px) 
        
    if keys[pygame.K_q]:
        pygame.quit()
        game.run=False

pygame.quit()

print("Saving data")

# Purge duplicates from long clicks
bluecarlist=list(dict.fromkeys(bluecarlist))
# print(bluecarlist)
with open('car_positions_'+difficulty+'.data','wb') as filehandle:
    pickle.dump(bluecarlist,filehandle)
    print("Data saved")
