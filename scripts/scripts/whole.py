#!/usr/bin/python2

import os
import sys
import rospy
import baxter_interface
from gtts import gTTS
import actionlib
from control_msgs.msg import (
    GripperCommandAction,
    GripperCommandGoal,
    SingleJointPositionAction,
    SingleJointPositionGoal,
    FollowJointTrajectoryAction,
    FollowJointTrajectoryGoal,
)
import speech_recognition as sr
from shutil import copyfile
import subprocess
import time
import baxter_core_msgs
from baxter_core_msgs.msg import AssemblyState
from std_msgs.msg import String
import baxter_external_devices
from baxter_interface import CHECK_VERSION


rospy.init_node('whole')

rs = baxter_interface.RobotEnable(baxter_interface.CHECK_VERSION)

right_gripper = baxter_interface.Gripper('right')
left_gripper = baxter_interface.Gripper('left')

limb_right = baxter_interface.Limb('right')
angles_right = limb_right.joint_angles()

limb_left = baxter_interface.Limb('left')
angles_left = limb_left.joint_angles()

angles_right['right_s0']=0.08 # untuck position right arm
angles_right['right_s1']=-1.0
angles_right['right_e0']=1.19
angles_right['right_e1']=1.94
angles_right['right_w0']=-0.67
angles_right['right_w1']=1.03
angles_right['right_w2']=0.50

angles_left['left_s0']=0.0 # untuck position left arm
angles_left['left_s1']=0.0
angles_left['left_e0']=0.0
angles_left['left_e1']=0.0
angles_left['left_w0']=0.0
angles_left['left_w1']=0.0
angles_left['left_w2']=0.0


step1 = 5 #step related to driving module
size1 = 0
direction1 = 1


d_recorder1 = 'rosrun baxter_examples joint_recorder.py -f driving_recorder1.txt'
d_recorder2 = 'rosrun baxter_examples joint_recorder.py -f driving_recorder2.txt'
d_recorder3 = 'rosrun baxter_examples joint_recorder.py -f driving_recorder3.txt'

d_player1 = 'rosrun baxter_examples joint_trajectory_file_playback.py -f driving_recorder1.txt'
d_player2 = 'rosrun baxter_examples joint_trajectory_file_playback.py -f driving_recorder2.txt'
d_player3 = 'rosrun baxter_examples joint_trajectory_file_playback.py -f driving_recorder3.txt'



## Mode parameters
driving_action = False
standard = False
player = False
manual = True

start = True

right = baxter_interface.Gripper('right', CHECK_VERSION)
left = baxter_interface.Gripper('left', CHECK_VERSION)

accept_state = True


while start:
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)


    try:

        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
        a = r.recognize_google(audio)
        print type (r.recognize_google(audio))

        a.encode('ascii','ignore')

        print a

        if a == 'hello Tony' or a == 'Hello Tony' :
            rs.enable()
            accept_state = True
            #process = subprocess.Popen('python call_back1.py', shell=True)
            #time.sleep(1)
            #process.terminate()
            os.system("mpg321 ready.mp3")
            break



    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


while start:
    
    #print 'Which mode do you want to use?'
    os.system("mpg321 choose.mp3")    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)


    try:

        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
        phrase = r.recognize_google(audio)
        #print type (r.recognize_google(audio))

        phrase.encode('ascii','ignore')

        all_words = phrase.split(' ')
        words = phrase.split(' ')
        for i in range(len(words)):
	        words[i] = str(words[i])
	        all_words[i] = str(all_words[i])
	        print all_words[i]

        print 'the phrase is:',phrase


        if 'driving' in words:
            driving_action = True
            os.system("mpg321 driving.mp3")
            start = False
            break

        elif 'standard' in words:
            standard = True
            os.system("mpg321 standard.mp3")
            start = False
            break

        elif 'user' in words:
            player = True
            os.system("mpg321 custom.mp3")
            start = False
            break




    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    #os.system("mpg321 real.mp3")


## MODE: Driving actions #################################################

driving_right = False
driving_left = False

#print 'Which arm do you want to control?'


while driving_action:
    os.system("mpg321 arm.mp3")


    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
        

    try:

        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))

        phrase = r.recognize_google(audio)
        #print type (r.recognize_google(audio))

        phrase.encode('ascii','ignore')

        all_words = phrase.split(' ')
        words = phrase.split(' ')
        for i in range(len(words)):
	        words[i] = str(words[i])
	        all_words[i] = str(all_words[i])
	        #print all_words[i]

        print 'the phrase is:',phrase

        if 'right' in words :
            driving_right = True
            #print 'right arm'
            break
        elif 'left' in words :
            driving_left = True
            break


    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


while driving_right: 
    
    os.system("mpg321 joint.mp3")

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
      

    try:

        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))


        phrase = r.recognize_google(audio)
        #print type (r.recognize_google(audio))

        phrase.encode('ascii','ignore')

        all_words = phrase.split(' ')
        words = phrase.split(' ')
        for i in range(len(words)):
	        words[i] = str(words[i])
	        all_words[i] = str(all_words[i])
	        #print all_words[i]

        print 'the phrase is:',phrase

        print 'Which joint do you want to control?'

        if 'one' in words:
            print 'Default value five degree'
            while True:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Say something!")
                    audio = r.listen(source)
                

                try:

                    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
                    a = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    a.encode('ascii','ignore')

                    print a


                    phrase = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    phrase.encode('ascii','ignore')

                    all_words = phrase.split(' ')
                    words = phrase.split(' ')
                    for i in range(len(words)):
	                words[i] = str(words[i])
	                all_words[i] = str(all_words[i])
	                print all_words[i]

                    print 'the phrase is:',phrase

                    if 'go' in words:
                        angles_right['right_w2'] = angles_right['right_w2'] + (3.14/180)*direction1*(size1+step1)
                        limb_right.move_to_joint_positions(angles_right)
                        print 'Rotate'
                        print angles_right['right_w2']
                        
                    elif 'increase' in words:
                        size1 = size1 + 5
                        angles_right['right_w2'] = angles_right['right_w2'] + (3.14/180)*direction1*(size1+step1)
                        limb_right.move_to_joint_positions(angles_right)

                    elif 'change' in words:
                        direction1 = -1*direction1
                        size1 = 0
                        angles_right['right_w2'] = angles_right['right_w2'] + (3.14/180)*direction1*(size1+step1)
                        limb_right.move_to_joint_positions(angles_right)

                    
                    elif 'stop' in words:
                        size1 = 0
                        direction1 = 1
                        break

                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))


        elif 'two' in words:
            print 'Default value one degree'
            while True:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Say something!")
                    audio = r.listen(source)
                

                try:

                    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
                    a = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    a.encode('ascii','ignore')

                    print a


                    phrase = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    phrase.encode('ascii','ignore')

                    all_words = phrase.split(' ')
                    words = phrase.split(' ')
                    for i in range(len(words)):
	                words[i] = str(words[i])
	                all_words[i] = str(all_words[i])
	                print all_words[i]

                    print 'the phrase is:',phrase

                    if 'go' in words:
                        angles_right['right_w1'] = angles_right['right_w1'] + (3.14/180)*direction1*(size1+step1)
                        limb_right.move_to_joint_positions(angles_right)
                        print 'Rotate'
                        print angles_right['right_w1']
                        
                    elif 'increase' in words:
                        size1 = size1 + 5
                        angles_right['right_w1'] = angles_right['right_w1'] + (3.14/180)*direction1*(size1+step1)
                        limb_right.move_to_joint_positions(angles_right)

                    elif 'change' in words:
                        direction1 = -1*direction1
                        size1 = 0
                        angles_right['right_w1'] = angles_right['right_w1'] + (3.14/180)*direction1*(size1+step1)
                        limb_right.move_to_joint_positions(angles_right)

                    
                    elif 'stop' in words:
                        size1 = 0
                        direction1 = 1
                        break

                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))

        elif 'three' in words:
            print 'Default value one degree'
            while True:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Say something!")
                    audio = r.listen(source)
                

                try:

                    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
                    a = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    a.encode('ascii','ignore')

                    print a


                    phrase = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    phrase.encode('ascii','ignore')

                    all_words = phrase.split(' ')
                    words = phrase.split(' ')
                    for i in range(len(words)):
	                words[i] = str(words[i])
	                all_words[i] = str(all_words[i])
	                print all_words[i]

                    print 'the phrase is:',phrase

                    if 'go' in words:
                        angles_right['right_w0'] = angles_right['right_w0'] + (3.14/180)*direction1*(size1+step1)
                        limb_right.move_to_joint_positions(angles_right)
                        print 'Rotate'
                        print angles_right['right_w0']
                        
                    elif 'increase' in words:
                        size1 = size1 + 5
                        angles_right['right_w0'] = angles_right['right_w0'] + (3.14/180)*direction1*(size1+step1)
                        limb_right.move_to_joint_positions(angles_right)

                    elif 'change' in words:
                        os.system("mpg321 direction.mp3")
                        direction1 = -1*direction1
                        size1 = 0
                        angles_right['right_w0'] = angles_right['right_w0'] + (3.14/180)*direction1*(size1+step1)
                        limb_right.move_to_joint_positions(angles_right)

                    
                    elif 'stop' in words:
                        size1 = 0
                        direction1 = 1
                        break

                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))




        elif '4' in words:
            print 'Default value one degree'
            while True:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Say something!")
                    audio = r.listen(source)
                

                try:

                    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
                    a = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    a.encode('ascii','ignore')

                    print a


                    phrase = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    phrase.encode('ascii','ignore')

                    all_words = phrase.split(' ')
                    words = phrase.split(' ')
                    for i in range(len(words)):
	                words[i] = str(words[i])
	                all_words[i] = str(all_words[i])
	                print all_words[i]

                    print 'the phrase is:',phrase

                    if 'go' in words:
                        angles_right['right_e1'] = angles_right['right_e1'] + (3.14/180)*direction1*(size1+step1)
                        limb_right.move_to_joint_positions(angles_right)
                        print 'Rotate'
                        print angles_right['right_e1']
                        
                    elif 'increase' in words:
                        size1 = size1 + 5
                        angles_right['right_e1'] = angles_right['right_e1'] + (3.14/180)*direction1*(size1+step1)
                        limb_right.move_to_joint_positions(angles_right)

                    elif 'change' in words:
                        direction1 = -1*direction1
                        size1 = 0
                        angles_right['right_e1'] = angles_right['right_e1'] + (3.14/180)*direction1*(size1+step1)
                        limb_right.move_to_joint_positions(angles_right)

                    
                    elif 'stop' in words:
                        size1 = 0
                        direction1 = 1
                        break

                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))

        elif '5' in words:
            print 'Default value one degree'
            while True:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Say something!")
                    audio = r.listen(source)
                

                try:

                    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
                    a = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    a.encode('ascii','ignore')

                    print a


                    phrase = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    phrase.encode('ascii','ignore')

                    all_words = phrase.split(' ')
                    words = phrase.split(' ')
                    for i in range(len(words)):
	                words[i] = str(words[i])
	                all_words[i] = str(all_words[i])
	                print all_words[i]

                    print 'the phrase is:',phrase

                    if 'go' in words:
                        angles_right['right_e0'] = angles_right['right_e0'] + (3.14/180)*direction1*(size1+step1)
                        limb_right.move_to_joint_positions(angles_right)
                        print 'Rotate'
                        print angles_right['right_e0']
                        
                    elif 'increase' in words:
                        size1 = size1 + 5
                        angles_right['right_e0'] = angles_right['right_e0'] + (3.14/180)*direction1*(size1+step1)
                        limb_right.move_to_joint_positions(angles_right)

                    elif 'change' in words:
                        direction1 = -1*direction1
                        size1 = 0
                        angles_right['right_e0'] = angles_right['right_e0'] + (3.14/180)*direction1*(size1+step1)
                        limb_right.move_to_joint_positions(angles_right)

                    
                    elif 'stop' in words:
                        size1 = 0
                        direction1 = 1
                        break

                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))


        elif '6' in words:
            print 'Default value one degree'
            while True:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Say something!")
                    audio = r.listen(source)
                

                try:

                    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
                    a = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    a.encode('ascii','ignore')

                    print a


                    phrase = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    phrase.encode('ascii','ignore')

                    all_words = phrase.split(' ')
                    words = phrase.split(' ')
                    for i in range(len(words)):
	                words[i] = str(words[i])
	                all_words[i] = str(all_words[i])
	                print all_words[i]

                    print 'the phrase is:',phrase

                    if 'go' in words:
                        angles_right['right_s1'] = angles_right['right_s1'] + (3.14/180)*direction1*(size1+step1)
                        limb_right.move_to_joint_positions(angles_right)
                        print 'Rotate'
                        print angles_right['right_s1']
                        
                    elif 'increase' in words:
                        size1 = size1 + 5
                        angles_right['right_s1'] = angles_right['right_s1'] + (3.14/180)*direction1*(size1+step1)
                        limb_right.move_to_joint_positions(angles_right)

                    elif 'change' in words:
                        direction1 = -1*direction1
                        size1 = 0
                        angles_right['right_s1'] = angles_right['right_s1'] + (3.14/180)*direction1*(size1+step1)
                        limb_right.move_to_joint_positions(angles_right)

                    
                    elif 'stop' in words:
                        size1 = 0
                        direction1 = 1
                        break
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))


        elif '7' in words:
            print 'Default value one degree'
            while True:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Say something!")
                    audio = r.listen(source)
                

                try:

                    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
                    a = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    a.encode('ascii','ignore')

                    print a


                    phrase = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    phrase.encode('ascii','ignore')

                    all_words = phrase.split(' ')
                    words = phrase.split(' ')
                    for i in range(len(words)):
	                words[i] = str(words[i])
	                all_words[i] = str(all_words[i])
	                print all_words[i]

                    print 'the phrase is:',phrase

                    if 'go' in words:
                        angles_right['right_s0'] = angles_right['right_s0'] + (3.14/180)*direction1*(size1+step1)
                        limb_right.move_to_joint_positions(angles_right)
                        print 'Rotate'
                        print angles_right['right_s0']
                        
                    elif 'increase' in words:
                        size1 = size1 + 5
                        angles_right['right_s0'] = angles_right['right_s0'] + (3.14/180)*direction1*(size1+step1)
                        limb_right.move_to_joint_positions(angles_right)

                    elif 'change' in words:
                        direction1 = -1*direction1
                        size1 = 0
                        angles_right['right_s0'] = angles_right['right_s0'] + (3.14/180)*direction1*(size1+step1)
                        limb_right.move_to_joint_positions(angles_right)

                    
                    elif 'stop' in words:
                        size1 = 0
                        direction1 = 1
                        break
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))



        
        elif 'gripper' in words:
            #print 'gripper'
            while True:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Say something!")
                    audio = r.listen(source)
                

                try:

                    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
                    a = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    a.encode('ascii','ignore')

                    print a


                    phrase = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    phrase.encode('ascii','ignore')

                    all_words = phrase.split(' ')
                    words = phrase.split(' ')
                    for i in range(len(words)):
	                words[i] = str(words[i])
	                all_words[i] = str(all_words[i])
	                print all_words[i]

                    print 'the phrase is:',phrase

                    if 'open' in words:
                        for i in range(1000):
    
                            right.open()
                        process = subprocess.Popen('python call_back1.py', shell=True)
                        time.sleep(1)
                        process.terminate()
                        os.system("mpg321 open.mp3")

                        
                    elif 'close' in words:
                        for i in range(1000):
        
                            right.close()
                        #process = subprocess.Popen('python call_back1.py', shell=True)
                        #time.sleep(1)
                        #process.terminate()
                        os.system("mpg321 close.mp3")
                        p = subprocess.call(['rosrun', 'baxter_tools', 'tuck_arms.py','-u'])


                    elif 'stop' in words:
                        size1 = 1
                        direction1 = 1
                        break

                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))


        
        elif 'save' in words:         
                        
            while True:
                
                            
                print 'In which slot do you want to save?'

                r = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Say something!")
                    audio = r.listen(source)



                try:

                    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
                    a = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    a.encode('ascii','ignore')

                    print a

                    if a == 'one':
                        process = subprocess.Popen(d_recorder1, shell=True)
                        time.sleep(5)
                        process.terminate()
                        #in another shell
                        #rosrun baxter_interface joint_trajectory_action_server.py --mode velocity
                        break

                    if a == 'two':
                        
                        process = subprocess.Popen(d_recorder2, shell=True)
                        time.sleep(5)
                        process.terminate()                        
                        #in another shell
                        #rosrun baxter_interface joint_trajectory_action_server.py --mode velocity
                        break

                    if a == 'three':
                        
                        process = subprocess.Popen(d_recorder3, shell=True)
                        time.sleep(5)
                        process.terminate()                       
                         #in another shell
                        #rosrun baxter_interface joint_trajectory_action_server.py --mode velocity
                        break



                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))


        elif 'exit'in words:
            break


    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


while driving_left:
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
      

    try:

        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
        a = r.recognize_google(audio)
        print type (r.recognize_google(audio))

        a.encode('ascii','ignore')

        print a


        phrase = r.recognize_google(audio)
        print type (r.recognize_google(audio))

        phrase.encode('ascii','ignore')

        all_words = phrase.split(' ')
        words = phrase.split(' ')
        for i in range(len(words)):
	        words[i] = str(words[i])
	        all_words[i] = str(all_words[i])
	        print all_words[i]

        print 'the phrase is:',phrase

        print 'Which joint do you want to control?'

        if 'one' in words:
            print 'Default value one degree'
            while True:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Say something!")
                    audio = r.listen(source)
                

                try:

                    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
                    a = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    a.encode('ascii','ignore')

                    print a


                    phrase = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    phrase.encode('ascii','ignore')

                    all_words = phrase.split(' ')
                    words = phrase.split(' ')
                    for i in range(len(words)):
	                words[i] = str(words[i])
	                all_words[i] = str(all_words[i])
	                print all_words[i]

                    print 'the phrase is:',phrase

                    if 'go' in words:
                        angles_left['left_w2'] = angles_left['left_w2'] + (3.14/180)*direction1*(size1+step1)
                        limb_left.move_to_joint_positions(angles_left)
                        print 'Rotate'
                        print angles_left['left_w2']
                        
                    elif 'increase' in words:
                        size1 = size1 + 5
                        angles_left['left_w2'] = angles_left['left_w2'] + (3.14/180)*direction1*(size1+step1)
                        limb_left.move_to_joint_positions(angles_left)

                    elif 'change' in words:
                        direction1 = -1*direction1
                        size1 = 0
                        angles_left['left_w2'] = angles_left['left_w2'] + (3.14/180)*direction1*(size1+step1)
                        limb_left.move_to_joint_positions(angles_left)

                    
                    elif 'stop' in words:
                        size1 = 0
                        direction1 = 1
                        break

                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))


        elif 'two' in words:
            print 'Default value one degree'
            while True:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Say something!")
                    audio = r.listen(source)
                

                try:

                    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
                    a = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    a.encode('ascii','ignore')

                    print a


                    phrase = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    phrase.encode('ascii','ignore')

                    all_words = phrase.split(' ')
                    words = phrase.split(' ')
                    for i in range(len(words)):
	                words[i] = str(words[i])
	                all_words[i] = str(all_words[i])
	                print all_words[i]

                    print 'the phrase is:',phrase
                    if 'go' in words:
                        angles_left['left_w1'] = angles_left['left_w1'] + (3.14/180)*direction1*(size1+step1)
                        limb_left.move_to_joint_positions(angles_left)
                        print 'Rotate'
                        print angles_left['left_w1']
                        
                    elif 'increase' in words:
                        size1 = size1 + 5
                        angles_left['left_w1'] = angles_left['left_w1'] + (3.14/180)*direction1*(size1+step1)
                        limb_left.move_to_joint_positions(angles_left)

                    elif 'change' in words:
                        direction1 = -1*direction1
                        size1 = 0
                        angles_left['left_w1'] = angles_left['left_w1'] + (3.14/180)*direction1*(size1+step1)
                        limb_left.move_to_joint_positions(angles_left)

                    
                    elif 'stop' in words:
                        size1 = 0
                        direction1 = 1
                        break

                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))

        elif 'three' in words:
            print 'Default value one degree'
            while True:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Say something!")
                    audio = r.listen(source)
                

                try:

                    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
                    a = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    a.encode('ascii','ignore')

                    print a


                    phrase = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    phrase.encode('ascii','ignore')

                    all_words = phrase.split(' ')
                    words = phrase.split(' ')
                    for i in range(len(words)):
	                words[i] = str(words[i])
	                all_words[i] = str(all_words[i])
	                print all_words[i]

                    print 'the phrase is:',phrase

                    if 'go' in words:
                        angles_left['left_w0'] = angles_left['left_w0'] + (3.14/180)*direction1*(size1+step1)
                        limb_left.move_to_joint_positions(angles_left)
                        print 'Rotate'
                        print angles_left['left_w0']
                        
                    elif 'increase' in words:
                        size1 = size1 + 5
                        angles_left['left_w0'] = angles_left['left_w0'] + (3.14/180)*direction1*(size1+step1)
                        limb_left.move_to_joint_positions(angles_left)

                    elif 'change' in words:
                        direction1 = -1*direction1
                        size1 = 0
                        angles_left['left_w0'] = angles_left['left_w0'] + (3.14/180)*direction1*(size1+step1)
                        limb_left.move_to_joint_positions(angles_left)

                    
                    elif 'stop' in words:
                        size1 = 0
                        direction1 = 1
                        break

                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))




        elif 'four' in words:
            print 'Default value one degree'
            while True:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Say something!")
                    audio = r.listen(source)
                

                try:

                    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
                    a = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    a.encode('ascii','ignore')

                    print a


                    phrase = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    phrase.encode('ascii','ignore')

                    all_words = phrase.split(' ')
                    words = phrase.split(' ')
                    for i in range(len(words)):
	                words[i] = str(words[i])
	                all_words[i] = str(all_words[i])
	                print all_words[i]

                    print 'the phrase is:',phrase

                    if 'go' in words:
                        angles_left['left_e1'] = angles_left['left_e1'] + (3.14/180)*direction1*(size1+step1)
                        limb_left.move_to_joint_positions(angles_left)
                        print 'Rotate'
                        print angles_left['left_e1']
                        
                    elif 'increase' in words:
                        size1 = size1 + 5
                        angles_left['left_e1'] = angles_left['left_e1'] + (3.14/180)*direction1*(size1+step1)
                        limb_left.move_to_joint_positions(angles_left)

                    elif 'change' in words:
                        direction1 = -1*direction1
                        size1 = 0
                        angles_left['left_e1'] = angles_left['left_e1'] + (3.14/180)*direction1*(size1+step1)
                        limb_left.move_to_joint_positions(angles_left)

                    
                    elif 'stop' in words:
                        size1 = 0
                        direction1 = 1
                        break

                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))

        elif 'five' in words:
            print 'Default value one degree'
            while True:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Say something!")
                    audio = r.listen(source)
                

                try:

                    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
                    a = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    a.encode('ascii','ignore')

                    print a


                    phrase = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    phrase.encode('ascii','ignore')

                    all_words = phrase.split(' ')
                    words = phrase.split(' ')
                    for i in range(len(words)):
	                words[i] = str(words[i])
	                all_words[i] = str(all_words[i])
	                print all_words[i]

                    print 'the phrase is:',phrase

                    if 'go' in words:
                        angles_left['left_e0'] = angles_left['left_e0'] + (3.14/180)*direction1*(size1+step1)
                        limb_left.move_to_joint_positions(angles_left)
                        print 'Rotate'
                        print angles_left['left_e0']
                        
                    elif 'increase' in words:
                        size1 = size1 + 5
                        angles_left['left_e0'] = angles_left['left_e0'] + (3.14/180)*direction1*(size1+step1)
                        limb_left.move_to_joint_positions(angles_left)

                    elif 'change' in words:
                        direction1 = -1*direction1
                        size1 = 0
                        angles_left['left_e0'] = angles_left['left_e0'] + (3.14/180)*direction1*(size1+step1)
                        limb_left.move_to_joint_positions(angles_left)

                    
                    elif 'stop' in words:
                        size1 = 0
                        direction1 = 1
                        break

                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))


        elif 'six' in words:
            print 'Default value one degree'
            while True:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Say something!")
                    audio = r.listen(source)
                

                try:

                    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
                    a = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    a.encode('ascii','ignore')

                    print a


                    phrase = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    phrase.encode('ascii','ignore')

                    all_words = phrase.split(' ')
                    words = phrase.split(' ')
                    for i in range(len(words)):
	                words[i] = str(words[i])
	                all_words[i] = str(all_words[i])
	                print all_words[i]

                    print 'the phrase is:',phrase

                    if 'go' in words:
                        angles_left['left_s1'] = angles_left['left_s1'] + (3.14/180)*direction1*(size1+step1)
                        limb_left.move_to_joint_positions(angles_left)
                        print 'Rotate'
                        print angles_left['left_s1']
                        
                    elif 'increase' in words:
                        size1 = size1 + 5
                        angles_left['left_s1'] = angles_left['left_s1'] + (3.14/180)*direction1*(size1+step1)
                        limb_left.move_to_joint_positions(angles_left)

                    elif 'change' in words:
                        direction1 = -1*direction1
                        size1 = 0
                        angles_left['left_s1'] = angles_left['left_s1'] + (3.14/180)*direction1*(size1+step1)
                        limb_left.move_to_joint_positions(angles_left)

                    
                    elif 'stop' in words:
                        size1 = 0
                        direction1 = 1
                        break


                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))


        elif 'seven' in words:
            print 'Default value one degree'
            while True:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Say something!")
                    audio = r.listen(source)
                

                try:

                    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
                    a = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    a.encode('ascii','ignore')

                    print a


                    phrase = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    phrase.encode('ascii','ignore')

                    all_words = phrase.split(' ')
                    words = phrase.split(' ')
                    for i in range(len(words)):
	                words[i] = str(words[i])
	                all_words[i] = str(all_words[i])
	                print all_words[i]

                    print 'the phrase is:',phrase

                    if 'go' in words:
                        angles_left['left_s0'] = angles_left['left_s0'] + (3.14/180)*direction1*(size1+step1)
                        limb_left.move_to_joint_positions(angles_left)
                        print 'Rotate'
                        print angles_left['left_s0']
                        
                    elif 'increase' in words:
                        size1 = size1 + 5
                        angles_left['left_s0'] = angles_left['left_s0'] + (3.14/180)*direction1*(size1+step1)
                        limb_left.move_to_joint_positions(angles_left)

                    elif 'change' in words:
                        direction1 = -1*direction1
                        size1 = 0
                        angles_left['left_s0'] = angles_left['left_s0'] + (3.14/180)*direction1*(size1+step1)
                        limb_left.move_to_joint_positions(angles_left)

                    
                    elif 'stop' in words:
                        size1 = 0
                        direction1 = 1
                        break

                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))

        elif 'gripper' in words:
            print 'gripper'
            while True:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Say something!")
                    audio = r.listen(source)
                

                try:

                    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
                    a = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    a.encode('ascii','ignore')

                    print a


                    phrase = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    phrase.encode('ascii','ignore')

                    all_words = phrase.split(' ')
                    words = phrase.split(' ')
                    for i in range(len(words)):
	                words[i] = str(words[i])
	                all_words[i] = str(all_words[i])
	                print all_words[i]

                    print 'the phrase is:',phrase

                    if 'open' in words:
                        for i in range(1000):
    
                            left.open()
                        process = subprocess.Popen('python call_back1.py', shell=True)
                        time.sleep(1)
                        process.terminate()
                        
                    elif 'close' in words:
                        for i in range(1000):
        
                            left.close()
                        process = subprocess.Popen('python call_back1.py', shell=True)
                        time.sleep(1)
                        process.terminate()

                    elif 'stop' in words:
                        size1 = 1
                        direction1 = 1
                        break

                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))


        
        elif 'save' in words:         
                        
            while True:
                
                            
                print 'In which slot do you want to save?'

                r = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Say something!")
                    audio = r.listen(source)



                try:

                    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
                    a = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    a.encode('ascii','ignore')

                    print a

                    if a == 'one':
                        process = subprocess.Popen(d_recorder1, shell=True)
                        time.sleep(5)
                        process.terminate()
                        #in another shell
                        #rosrun baxter_interface joint_trajectory_action_server.py --mode velocity
                        break

                    if a == 'two':
                        
                        process = subprocess.Popen(d_recorder2, shell=True)
                        time.sleep(5)
                        process.terminate()                  
                        #in another shell
                        #rosrun baxter_interface joint_trajectory_action_server.py --mode velocity
                        break

                    if a == 'three':
                        
                        process = subprocess.Popen(d_recorder3, shell=True)
                        time.sleep(5)
                        process.terminate()                        
                        #in another shell
                        #rosrun baxter_interface joint_trajectory_action_server.py --mode velocity
                        break



                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))


        elif 'exit'in words:
            break


    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))



######### Mode: Standard actions ######################

while standard:
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)


    try:

        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
        phrase = r.recognize_google(audio)
        phrase.encode('ascii','ignore')

        #print type (r.recognize_google(audio))

        all_words = phrase.split(' ')
        words = phrase.split(' ')
        for i in range(len(words)):
	        words[i] = str(words[i])
	        all_words[i] = str(all_words[i])
	        #print all_words[i]

        #print 'the phrase is:',phrase

        if 'ready' in words or 'work' in words:
            #untuck arms
            p = subprocess.call(['rosrun', 'baxter_tools', 'tuck_arms.py','-u'])
        elif 'hand' in words or 'gripper' in words:
            
            if 'right' in words:
                if 'open' in words:
                    right.calibrate()
                    for i in range(10000):
            
                        right.open()
                    process = subprocess.Popen('python call_back1.py', shell=True)
                    time.sleep(1)
                    process.terminate()
               
                    #print 'right hand is open'
                elif 'close' in words:
                    for i in range(10000):
                
                        right.close()
                    process = subprocess.Popen('python call_back1.py', shell=True)
                    time.sleep(1)
                    process.terminate()

            elif 'left' in words:
                if 'open' in words:
                    for i in range(10000):
            
                        left.open()
                        os.system("mpg321 open.mp3")
               
                #left_gripper.open()
                    #print 'left hand is open'
                elif 'close' in words:
                    for i in range(1000):
                
                        left.close()
                        os.system("mpg321 close.mp3")
        elif 'arm' in words:
            if 'right' in words:
                #os.system("mpg321 agree.mp3")
                limb_right.move_to_joint_positions(angles_right)
                print 'right arm is open'
                os.system("mpg321 actionC.mp3")
            elif 'left' in words:
                #os.system("mpg321 agree.mp3")
                limb_left.move_to_joint_positions(angles_left)                 
                print 'left arm is open'
                os.system("mpg321 actionC.mp3")
        
        elif 'goodbye' in words:
            #tuck arms
            p = subprocess.call(['rosrun', 'baxter_tools', 'tuck_arms.py','-t'])
            os.system("mpg321 sleep.mp3")

            print 'Baxter is sleeping...'
   
                
                


    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    

### CUSTOM MODE ##################

f = open("reader.txt","r") #opens file with name of "reader.txt"
c = d = 0
middle = False
introduction = 2
for m in range(0,introduction):
	f.readline() ##skip the first two lines of the txt file
number = 0
p_exit = False

while player :
    
    os.system("mpg321 ch.mp3")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something user!")
        audio = r.listen(source)

    try:

        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
        phrase = r.recognize_google(audio)
        phrase.encode('ascii','ignore')

        all_words = phrase.split(' ')
        words = phrase.split(' ')
        for i in range(len(words)):
	        words[i] = str(words[i])
	        all_words[i] = str(all_words[i])
	        #print all_words[i]
    
        #print 'Do you want to play your actions or to create manually a new one?'
        
        if 'play' in words:
            #
            while True:
    
                os.system("mpg321 action.mp3")

                #print 'first action: reproduce an action recorded in the Driving module, second action: reproduce your own action insert by txt file, third action: reproduce your manual implemented movement'
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Say something!")
                    audio = r.listen(source)


                try:

                    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
                    phrase = r.recognize_google(audio)
                    print type (r.recognize_google(audio))

                    phrase.encode('ascii','ignore')

                    print phrase
                    all_words = phrase.split(' ')
                    words = phrase.split(' ')
                    for i in range(len(words)):
	                    words[i] = str(words[i])
	                    all_words[i] = str(all_words[i])
	                    #print all_words[i]

                    if 'first' in words:
                        #
                        while True:
                            #print 'Which slot do you want to reproduce?'
                            r = sr.Recognizer()
                            with sr.Microphone() as source:
                                print("Say something!")
                                audio = r.listen(source)
                            try:

                                print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
                                a = r.recognize_google(audio)
                                a.encode('ascii','ignore')

                                if a == 'one' :
                                    p = subprocess.call(['rosrun','baxter_examples','joint_trajectory_file_playback.py','-f','driving_recorder1.txt'])
                                    break

                                elif a == 'two' :
                                    p = subprocess.call(['rosrun','baxter_examples','joint_trajectory_file_playback.py','-f','driving_recorder2.txt'])
                                    break

                                elif a == 'three' :
                                    p = subprocess.call(['rosrun','baxter_examples','joint_trajectory_file_playback.py','-f','driving_recorder3.txt'])
                                    break



                            except sr.UnknownValueError:
                                print("Google Speech Recognition could not understand audio")
                            except sr.RequestError as e:
                                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                        
                        
                    elif 'second' in words:
                        #
                        number = input('Which custom command command do you want to use?')
                        while True:
                                
                            r = sr.Recognizer()
                            with sr.Microphone() as source:
                                print("Say something!")
                                audio = r.listen(source)


                            try:

                                print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
                                a = r.recognize_google(audio)
                                a.encode('ascii','ignore')

                                if a == 'one' :
                                    number = 1
                                    break

                                elif a == 'two' :
                                    number = 2
                                    break

                                elif a == 'three' :
                                    number = 3
                                    break

                                elif a == 'four' :
                                    number = 4
                                    break

                                elif a == 'five' :
                                    number = 5
                                    break



                            except sr.UnknownValueError:
                                print("Google Speech Recognition could not understand audio")
                            except sr.RequestError as e:
                                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                        



                        for n in range(0,number-introduction-1):
    	                    f.readline()

                        sentence = f.readline()
                        print sentence

                        keywords = []
                        shell_command = []

                        words = sentence.split(' ')
                        for i in range(len(words)):
	                        words[i] = str(words[i])
	                        print words[i]

                        
                        for j in range(len(words)):
                            if words[j] == ';':
                                middle = True
                                print 'luca'
                                print j
                                
                            elif middle == False:		
                                keywords.append(words[j])
                                print 'mario'
                                print keywords[c]
                                c += 1
                            else:
                                if words[j] == '.' or words[j] == '.\n':
                                    break
                                shell_command.append(words[j])
                                print 'sandro'
                                d +=1

                        print keywords
                        print shell_command
                    	subprocess.call(shell_command)


                    if 'third' in words:
                        
                        while True:
                            os.system("mpg321 play.mp3")
                                
                            r = sr.Recognizer()
                            with sr.Microphone() as source:
                                print("Say something!")
                                audio = r.listen(source)


                            try:

                                print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
                                a = r.recognize_google(audio)
                                a.encode('ascii','ignore')

                                if a == 'one' :
                                    p = subprocess.call(['rosrun','baxter_examples','joint_trajectory_file_playback.py','-f','manual_recorder1.txt'])
                                    break

                                elif a == 'two' :
                                    p = subprocess.call(['rosrun','baxter_examples','joint_trajectory_file_playback.py','-f','manual_recorder2.txt'])
                                    break

                                elif a == 'three' :
                                    p = subprocess.call(['rosrun','baxter_examples','joint_trajectory_file_playback.py','-f','manual_recorder3.txt'])
                                    break

                                elif a == 'four' :
                                    p = subprocess.call(['rosrun','baxter_examples','joint_trajectory_file_playback.py','-f','manual_recorder4.txt'])
                                    break

                                elif a == 'five' :
                                    p = subprocess.call(['rosrun','baxter_examples','joint_trajectory_file_playback.py','-f','manual_recorder5.txt'])
                                    break



                            except sr.UnknownValueError:
                                print("Google Speech Recognition could not understand audio")
                            except sr.RequestError as e:
                                print("Could not request results from Google Speech Recognition service; {0}".format(e))
         


                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))

        elif 'create' in words:
            manual = True
            break            

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


enable_save = False
m_exit = False
array = 'rosrun baxter_examples joint_recorder.py -f manual_recorder.txt'

if manual:
    os.system("mpg321 rec.mp3")
    process = subprocess.Popen('rosrun baxter_examples joint_recorder.py -f manual_recorder.txt', shell=True)
    time.sleep(30)
    process.terminate()
  

while manual:
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)


        try:

            print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
            a = r.recognize_google(audio)
            a.encode('ascii','ignore')

            if a == 'stop':
                #process.terminate()
                enable_save = True
                break



        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

            
    if enable_save == True :
            
        #print'Do you want to save this movement?'

        while True:
            
            os.system("mpg321 mov.mp3")

            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Say something!")
                audio = r.listen(source)


            try:

                print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
                a = r.recognize_google(audio)
                a.encode('ascii','ignore')

                if a == 'yes':
                    #print'In which slot number, from 1 to 5?'
                    os.system("mpg321 slot.mp3")

                    while True:
    
                        r = sr.Recognizer()
                        with sr.Microphone() as source:
                            print("Say something!")
                            audio = r.listen(source)


                        try:

                            print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
                            a = r.recognize_google(audio)
                            a.encode('ascii','ignore')

                            if a == 'one':
                                copyfile('manual_recorder.txt','manual_recorder1.txt')
                                os.system("mpg321 rep.mp3")
                                p = subprocess.call(['rosrun','baxter_examples','joint_trajectory_file_playback.py','-f','manual_recorder1.txt'])
                                m_exit = True
                                break
                                
                            if a == 'two':
                                copyfile('manual_recorder.txt','manual_recorder2.txt')
                                os.system("mpg321 rep.mp3")
                                p = subprocess.call(['rosrun','baxter_examples','joint_trajectory_file_playback.py','-f','manual_recorder2.txt'])
                                m_exit = True
                                break        

                            if a == 'three':
                                copyfile('manual_recorder.txt','manual_recorder3.txt')
                                os.system("mpg321 rep.mp3")
                                p = subprocess.call(['rosrun','baxter_examples','joint_trajectory_file_playback.py','-f','manual_recorder3.txt'])
                                m_exit = True
                                break
                                
                            if a == 'four':
                                copyfile('manual_recorder.txt','manual_recorder4.txt')
                                os.system("mpg321 rep.mp3")
                                p = subprocess.call(['rosrun','baxter_examples','joint_trajectory_file_playback.py','-f','manual_recorder4.txt'])
                                m_exit = True
                                break 

                            if a == 'five':
                                copyfile('manual_recorder.txt','manual_recorder5.txt')
                                os.system("mpg321 rep.mp3")
                                p = subprocess.call(['rosrun','baxter_examples','joint_trajectory_file_playback.py','-f','manual_recorder5.txt'])
                                m_exit = True
                                break        


                        except sr.UnknownValueError:
                            print("Google Speech Recognition could not understand audio")
                        except sr.RequestError as e:
                            print("Could not request results from Google Speech Recognition service; {0}".format(e))

                if a == 'no':
                    m_exit == True
                    break

                if m_exit == True:
                    break

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

                
        if m_exit == True:
            break


