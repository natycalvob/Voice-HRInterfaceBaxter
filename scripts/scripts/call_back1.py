#!/usr/bin/python2

import os
import sys
import rospy
import baxter_interface
import subprocess
import baxter_core_msgs
from baxter_core_msgs.msg import AssemblyState
from std_msgs.msg import String
from baxter_core_msgs.msg import EndEffectorState
from gtts import gTTS


#closed = ("The gripper is closed")
#tts = gTTS(text = closed, lang='en')
#tts.save("close.mp3")

#opened = ("The gripper is open")
#tts = gTTS(text = opened, lang='en')
#tts.save("open.mp3")

a = 70

global en
en = True

#topic type: /robot/end_effector/right_gripper/state

 
def callback(data):
    global en
    
    #rospy.loginfo( data.position)
    #print data.position
    if data.position < 70 and en:
        os.system("mpg321 close.mp3")
        en = False
        
    if data.position > 70 and en:
        os.system("mpg321 open.mp3")
        en = False
        


     
def listener():

    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("robot/end_effector/left_gripper/state", EndEffectorState , callback)
 
    rospy.spin()
 
if __name__ == '__main__':
    listener()


