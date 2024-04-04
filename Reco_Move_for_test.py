'''
Reco DONE
Move DONE
DETECT DONE

'''

from naoqi import ALProxy
import time

nao_ip = "192.168.1.35"
nao_port = 9559

motion = ALProxy("ALMotion", nao_ip, nao_port)
motion.wakeUp()

posture = ALProxy('ALRobotPosture', nao_ip, nao_port)
posture.goToPosture("Stand", 1.0)

motion.moveInit()
motion.stiffnessInterpolation("Body", 1.0, 1.0)

# touch sensors
memory = ALProxy("ALMemory", nao_ip, nao_port)

# sonar for touch detection
sonar = ALProxy("ALSonar", nao_ip, nao_port)
sonar.subscribe("SonarApp")

speechRecognition = ALProxy("ALSpeechRecognition", nao_ip, nao_port)
speechRecognition.pause(True)
speechRecognition.setLanguage("English")
speechRecognition.setVocabulary(["green", "red"], False)

for i in range(5):
    print("Listening", i)
    speechRecognition.subscribe("ASR")
    
    speechRecognition.pause(False)
    time.sleep(8)
    speechRecognition.pause(True)
    
    words = memory.getData("WordRecognized")
    print("Word: ", words)

    if "green" in words:
        print('Moving forward')
        motion.moveInit()
        while True:
            # Check dis
            distance = memory.getData("Device/SubDeviceList/US/Right/Sensor/Value")
            # Check if touch
            headTouched = memory.getData("Device/SubDeviceList/Head/Touch/Middle/Sensor/Value")
            
            if distance < 0.1 or headTouched:  # assuming 0.5 meters as threshold
                print("Obstacle detected, stopping")
                motion.stopMove()
                break
            
            # motion.post.moveTo(0.2, 0.0, 0.0)  # Adjust speed as needed

            motion.post.moveTo(0.002, 0.0, 0.0)
            time.sleep(2)

            motion.post.moveTo(0.002, 0.0, 0.0)
            time.sleep(2)

            motion.post.moveTo(0.002, 0.0, 0.0)
            time.sleep(2)

            motion.post.moveTo(0.002, 0.0, 0.0)

    elif "red" in words:
        print('Stopping')
        motion.stopMove()

    speechRecognition.unsubscribe("ASR")

# Clean up
sonar.unsubscribe("SonarApp")
motion.stiffnessInterpolation("Body", 0, 1.0)
 
        motion.stopMove()  
        motion.post.moveTo(0.0, 0.0, 0.0)

        # lower speed
        # init motion before loop
