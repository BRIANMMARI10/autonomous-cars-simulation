# Import Python functions
import pygame
import pickle
from time import time
import math
import random

# Import our own functions
from classes import car
from window_class import Window, World, car_game
import statespace
import motionplanning
import logResults

manuallyAddCars=False
difficulty="Easy" #Easy, Medium, Hard, Extreme, Random
photoMode=False

if manuallyAddCars == True:
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
world=World(game,manuallyAddCars,photoMode) # Generate world

# print("Generating roadmap for solver")
# Map = statespace.RoadMap(game, world)
# print("Attempting to solve")
# planner = motionplanning.SamplingPlanner(Map,game)
# t0 = time()
# solved, plan, exploredNodes, _ = planner.RRT(game)
# t1 = time() 
# if solved: 
#     print(f'Path found in {t1-t0} s\n')
# else:
#     print('Path not found')

# motionplanning.Simulation(Map, game, plan, exploredNodes)
# # logResults(plan, Map) 

actions = [] # L for left lane change, R for right lane change, number for seconds going straight

for i in range(10):
    act = random.randint(0,2)
    if act == 0:
        actions.append('L')
    if act == 1:
        actions.append('R')
    if act == 2:
        t = random.randint(1,5)
        actions.append(t)

print(actions)

busy = False
angle = 0
turn_increment = 15

# Run the game
while game.run:
    game.clock.tick(100)

    # Update green cars
    for active_car in game.active_list:
        active_car.spritex+=active_car.vel
        active_car.updateCarOrigin()

    # Get new events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.run = False

    keys = pygame.key.get_pressed()

    t = pygame.time.get_ticks()

    if not busy and actions:
        action = actions.pop(0)
        start_time = t
        busy = True

        if action == 'L':
            angle = turn_increment
            lane_change_time = 1.32
        elif action == 'R':
            angle = -turn_increment
            lane_change_time = 1.4
        else:
            angle = 0

    if angle != 0:
        if t-start_time <= ((lane_change_time)*1000)/2:
            game.orange_car.turnCar(angle)  
        elif game.orange_car.theta*(angle/abs(angle)) > 0:
            game.orange_car.turnCar(-angle)
        else:
            game.orange_car.theta = 0
            busy = False 

    elif angle == 0:
        if t-start_time <= action*1000:
            game.orange_car.turnCar(angle)
        else:
            busy = False
    
    if manuallyAddCars:
    # Get cursor position for placing blue cars
        cursor=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        if click[0]==1:
            window_pos=(world.window.x,world.window.y)
            cursor_pos=(cursor[0]+window_pos[0],cursor[1]+window_pos[1])
            new_obst=car(cursor_pos[0],cursor_pos[1],"obstacle")
            game.obst_list.add(new_obst)
            game.all_sprites.add(new_obst)
            bluecarlist.append(cursor_pos)

    world.updateWinPos(game)
    world.window.redrawGameWindow(game,world.WorldSize_px) 
        
    if keys[pygame.K_q]:
        pygame.quit()
        game.run=False

pygame.quit()

if manuallyAddCars:
    print("Saving data")

    # Purge duplicates from long clicks
    bluecarlist=list(dict.fromkeys(bluecarlist))
    # print(bluecarlist)
    with open('car_positions_'+difficulty+'.data','wb') as filehandle:
        pickle.dump(bluecarlist,filehandle)
        print("Data saved")
