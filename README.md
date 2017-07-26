# Voice-HRInterfaceBaxter
Voice Recognition Interface integrated in ROS using the Baxter Robot

## baxter_action Package 

## What is baxter_actions ?

baxter_action is a ros package designed to be used with the speech recognition interface in order to generate a conversational environment with the user. This interface has been integrated in ROS, using the Baxter Robot, the user could execute different tasks. 
baxter_actions generates an interface which recieves voice commands from a user, processes the information and generate a set of actions in accordance with the user's requirements. 

This package has been tested with ros indigo.

## How to use baxter_actions Package ?

First, make sure you have all the requirements listed in the "Requirements" section.
launch Baxter Workstation Setup 
launch rosrun baxter_actions whole.py 
Follow the documentation located in the src folder

## Important!

Depending on the action that the user develops, some action_service must be run in the background in order to perform the tasks required for the user. Ensure running the server before executing the action.
 
## Requirements

To use all of the functionality of the interface, ensure that the system has:

ROS Indigo 
Python 2.6, 2.7, or 3.3+ 
PyAudio 0.2.11+ 
gTTS (Google Text to Speech)
mpg321 (.mp3 player)
