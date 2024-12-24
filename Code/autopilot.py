# Import Python functions
import pygame
import pickle
from time import time
import math
import random
import sys
import argparse
import matplotlib.pyplot as plt

# Import our own functions
sys.path.append('Game/')
sys.path.append('MotionPlanning/')
from car import car
from window import Window
from world import World
from game import car_game
import statespace
import motionplanner

# Global metrics
collisions_per_simulation = []  # To store collision counts for each simulation

def main(planner_type):
    global collisions_per_simulation 
    difficulty="Easy" #Easy, Medium, Hard, Extreme, Random

    # Launch Game
    print("Starting game")
    game=car_game(difficulty) # Instantiate game
    print("Generating world")
    world=World(game) # Generate world

    # Generate Motion Plan
    print("Generating roadmap for solver")
    Map = statespace.RoadMap(game, world)
    print("Attempting to solve")
    planner = None
    t0 = time()
    solved, plan, exploredNodes, _ = None, None, None, None

    if planner_type == 'RRT':
        planner = motionplanner.SamplingPlanner(Map)
        solved, plan, exploredNodes, _ = planner.RRT()
    elif planner_type == 'Astar':
        planner = motionplanner.GridPlanner(Map)
        solved, plan, exploredNodes, _ = planner.Astar()
    elif planner_type == 'Dijkstra':
        planner = motionplanner.GridPlanner(Map)
        solved, plan, exploredNodes, _ = planner.Dijkstra()
    elif planner_type == 'BFS':
        planner = motionplanner.GridPlanner(Map)
        solved, plan, exploredNodes, _ = planner.BFS()
    elif planner_type == 'DFS':
        planner = motionplanner.GridPlanner(Map)
        solved, plan, exploredNodes, _ = planner.DFS()
    else:
        print(f"Error: Unsupported planner type '{planner_type}'")
        return


    t1 = time() 
    if solved: 
        print(f'Path found in {t1-t0} s\n')
    else:
        print('Path not found')
    planner.simulation(plan, exploredNodes)
    actions = motionplanner.actionPlanner_SDC(Map, plan)

    # Run Game in Autopilot Mode
    collisions = runGame(game, world, actions, Map)
    collisions_per_simulation.append(collisions)  # Append collision count for this simulation
    
    pygame.quit()

def runGame(game, world, actions, roadmap):
    busy = False
    ready_for_next_action = True
    angle = 0
    turn_increment = 15
    count, start_count =0, 0
    collision_detected = False  # To track if a collision has occurred
    collision_count = 0

    while game.run:
        game.clock.tick(100)
        count+=1

        # Update green cars
        for active_car in game.active_list:
            active_car.spritex+=active_car.vel
            active_car.updateCarOrigin()

         # Check for collisions
        orange_car_position = (game.orange_car.spritex + game.orange_car.car_width_px / 2,
                               game.orange_car.spritey + game.orange_car.car_height_px / 2)

        if not roadmap.collisionAvoidance(orange_car_position):
            if not collision_detected:  # Count collision only once per detection
                print("Collision Detected!")
                collision_detected = True  # Mark collision as detected
                collision_count += 1  # Increment global collision count
                
        else:
            # Reset the flag if no collision is currently detected
            collision_detected = False



        # Get new events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.run = False

        keys = pygame.key.get_pressed()

        # t = pygame.time.get_ticks()
        
        # Autopilot actions
        if ready_for_next_action:
            if actions:
                action,position = actions.pop(0)
                ready_for_next_action = False

                if action == 'L':
                    angle = turn_increment
                    lane_change_count = 33
                elif action == 'R':
                    angle = -turn_increment
                    lane_change_count = 33

        if game.orange_car.x + 3*game.orange_car.car_width_px < position:
            game.orange_car.turnCar(0,game)
            start_count = count
        else:
            if count-start_count<=lane_change_count:
                game.orange_car.turnCar(angle,game)  
            elif game.orange_car.theta*(angle/abs(angle)) > 0:
                game.orange_car.turnCar(-angle,game)
            else:
                game.orange_car.theta = 0
                ready_for_next_action = True

        world.updateWinPos(game)
        world.window.skyView(game)
            
        if keys[pygame.K_q]:
            pygame.quit()
            game.run=False
    return collision_count

if __name__ == '__main__':
     # Argument parser for selecting the planner
    parser = argparse.ArgumentParser(description="Run car simulation with specified motion planner.")
    parser.add_argument(
        '--planner',
        type=str,
        default='RRT',
        choices=['RRT', 'Astar', 'Dijkstra', 'BFS', 'DFS'],
        help="Specify the planner to use (RRT, A*, Dijkstra, BFS, DFS). Default is RRT."
    )
    args = parser.parse_args()
    num_simulations = 10  # Number of runs
    for _ in range(num_simulations):
        main(args.planner)
    # Plot collisions vs. simulation number
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, num_simulations + 1), collisions_per_simulation, marker='o', linestyle='-', color='blue', label='Collisions')
    plt.xlabel('Simulation Number')
    plt.ylabel('Number of Collisions')
    plt.title('Collisions vs. Simulation Number')
    plt.legend()
    plt.grid(True)
    plt.show()

