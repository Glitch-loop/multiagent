# What is a multiagent system? :robot:
A multi-agent system is a system composed of many "agents" that interact with each other and are in the same environment.

## The multiagent systems are conformed by:
- Agent:
  - There can be N agents in the system.
  - Each agent has a behavior (this behavior must be directed to achieve a goal or task).
  - An agent can interact with another agent
  - An agent must decide to carry out an action, this according to the environment and the agents that are around him at that moment.

- Enviroment
  - Can be *static* (does not change through steps)
  - Can be *dynamic* (changes through steps)
  - The environment can have initial values.

> Note: This kind of model is executed by steps (we can see it like a cycle in a for loop)

# What would I use multiagent system for? :speech_balloon:
This type of model is used to simulate environments in which there are many actors and they interact with each other.
It is commonly used in *social sciences* where there are multiple scenarios made up of an environment and multiple agents (for example, the stock market).


# What are I going to find in this repo? :eye_speech_bubble:
1- Cleaner robot homework, it is coded to use with `Jupyter notebook`

2 - Design of the multiagent system deliverable, it was coded for use with `Jupyter notebook`

3 - Implementation of our multiagent system in a python server, we used `Flask` to create the server

## What is the main project of our repository? :100:
The project tries to simulate an intersection in which each lane has its traffic light, upon reaching the center and if the traffic light is green, each agent will make the decision to go straight, turn right or turn left. , being careful not to hit any cars (in this case, the agent must stop and wait until the road is clear to proceed).
The main project is in the file *"integradora2"*.
We used heroku to implement it, the engine we used to run the flask server on heroku was `gunicorn`

The library that allows us to simulate the intersection was `agentpy`

If you want to visualize the output of the simulation, then (for ease) you should run it in the `jupyter notebook` project and it will use `matplot` to render the plots

