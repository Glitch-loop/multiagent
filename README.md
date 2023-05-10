# What is a multiagent system?
A multiagent system is a system compouse for many "agents" that interarct between themselves and are in a same enviroment.

## The multiagent systems are conformed by:
- Agent:
  - It can be N agents in the system
  - Each agent have a behaviour (this behaviour should be directed to achive a goal or task).
  - An agent can interacts with another agent
  - An agent must decide to perform an action, this according with the enviroment and the agents that are around of him currently.

- Enviroment
  - It can be static (It doesn't change through the steps)
  - It can be dynamic (It changes through the steps)
  -The enviroment might have initial values.

> Note: This kind of model is executed by steps (we can see it like a cycle in a for loop)

# What would I use multiagent system for?
This kind of model is used to simulate enviroments which there are many actors and they are interact with themselves. 
It is common used in *social sciences* where a multiple scenarios which are compoused for a enviroment and multiple agents (e.g. Stock market).

# What are I going to find in this repo?
1- Homework Cleaner robot, it was coding for use with `Jupyter notebook`

2 - Design of the multiagent system deliverable, it was coding for use with `Jupyter notebook`

3 - Implementation of our multiagent system in a python server, to create the server we used `Flask`

## What is the main project of our repository?
The project deals with simulating an intersection in which each lane has its traffic light, upon reaching the center and if the traffic light is green, each agent will make the decision to go straight, turn right or turn left. , taking care not to collide with any car (in this case the agent must stop to wait until the road is clear to move forward).
