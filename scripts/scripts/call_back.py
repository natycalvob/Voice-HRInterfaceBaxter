#!/usr/bin/python2

import os
import sys
import rospy
import baxter_interface
import subprocess
import baxter_core_msgs
from baxter_core_msgs.msg import AssemblyState
from std_msgs.msg import String
import subprocess
from gtts import gTTS

#readytowork = ("Hello Sir, I am ready to work, please give any instruction")
#tts = gTTS(text = readytowork, lang='en')
#tts.save("ready.mp3")


#from baxter_core_msgs import AssemblyState


#topic type: baxter_core_msgs/AssemblyState
global en 
en = True
def callback(data):
    
    global en
    if en and data.enabled:
        print data.enabled
        os.system("mpg321 ready.mp3")
        en = False

    rospy.on_shutdown
def listener():

    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("robot/state", AssemblyState , callback)

    rospy.spin()
 
if __name__ == '__main__':
    listener()


