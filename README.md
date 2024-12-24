# Self-Driving Car Simulation: Path Planning and Camera Enhancements

This project builds on the repository [ENPM661 Project 5](https://github.com/BrianBock/ENPM661-Project-5), which implements the various path-planning algorithms for a self-driving car, including:
- **RRT** (Rapidly-Exploring Random Tree)
- **A\*** (A-Star)
- **Dijkstra**
- **BFS** (Breadth-First Search)
- **DFS** (Depth-First Search)

## My Contributions
- **Sky View Mode**:
  - Added a new camera mode that provides a fixed, bird's-eye view of the entire track for better visualization of simulations.
  
- **Algorithm Simulations & Performance Metrics**:
  - Wrote a collision detection function to evaluate and characterize the performance of each algorithm
  - Conducted  simulations across multiple grid-based planners (A*, Dijkstra, BFS, DFS) and assessed their behavior over a ten simulation runs
  
### Performance Graphs
#### 1. **RRT Performance**
  - ![RRT Performance](./assets/RRT_collisions.png)
    
#### 2. **A* Performance**
![A* Performance](./assets/Astar_collisions.png)

#### 3. **Dijkstra Performance**
![Dijkstra Performance](./assets/Dijkstra_collisions.png)

#### 4. **Breadth-First Search Performance**
![Breadth-First Search Performance](./assets/BFS_collisions.png)

#### 5. **Depth-First Search Performance**
![Depth-First Search Performance](./assets/DFS_collisions.png)

- **Next Steps:
  - Use Reinforcement Learning to fine-tune parameters for all the various path-planning algorithms I implemented. 
