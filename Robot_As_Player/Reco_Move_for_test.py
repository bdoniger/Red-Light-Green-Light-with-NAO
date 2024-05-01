'''
RECO, MOVE, DETECTION DONE
KEEP MOVING UNDER GREEN UNTIL RED
KEEP STATIC UNDER RED UNTIL GREEN
'''


from naoqi import ALProxy
import time

nao_ip = "192.168.1.35"
nao_port = 9559

# Initialize proxies
motion = ALProxy("ALMotion", nao_ip, nao_port)
posture = ALProxy("ALRobotPosture", nao_ip, nao_port)
memory = ALProxy("ALMemory", nao_ip, nao_port)
sonar = ALProxy("ALSonar", nao_ip, nao_port)
speechRecognition = ALProxy("ALSpeechRecognition", nao_ip, nao_port)

# Set up robot
motion.wakeUp()
posture.goToPosture("Stand", 1.0)
motion.moveInit()
motion.stiffnessInterpolation("Body", 1.0, 1.0)
sonar.subscribe("SonarApp")

# Set up speech recognition
speechRecognition.pause(True)
speechRecognition.setLanguage("English")
speechRecognition.setVocabulary(["green", "red"], False)

is_moving = False

while True:
    print("Listening for 'green' or 'red'")
    speechRecognition.subscribe("ASR")
    speechRecognition.pause(False)
    time.sleep(5)
    speechRecognition.pause(True)
    words = memory.getData("WordRecognized")
    speechRecognition.unsubscribe("ASR")

    print("Heard:", words)

    if "red" in words and is_moving:
        print('Stopping')
        motion.stopMove()
        is_moving = False

    elif "green" in words and not is_moving:
        print('Starting to move')
        is_moving = True

        while is_moving:
            distance = memory.getData("Device/SubDeviceList/US/Right/Sensor/Value")
            headTouched = memory.getData("Device/SubDeviceList/Head/Touch/Middle/Sensor/Value")

            if distance < 0.1 or headTouched:
                print("Obstacle detected, stopping")
                motion.stopMove()
                is_moving = False
                break

            motion.post.moveTo(0.002, 0.0, 0.0)
            time.sleep(1)

            # =====================================
            memory = ALProxy("ALMemory", nao_ip, nao_port)
            print("Listening for 'green' or 'red' during movement")
            speechRecognition.subscribe("ASR")
            speechRecognition.pause(False)
            time.sleep(2)
            speechRecognition.pause(True)
            
            words = memory.getData("WordRecognized")
            speechRecognition.unsubscribe("ASR")

            print(" during movement Heard:", words)

            if "red" in words and is_moving:
                print('Stopping')
                motion.stopMove()
                is_moving = False
            # =====================================


# Clean up
sonar.unsubscribe("SonarApp")
motion.stiffnessInterpolation("Body", 0, 1.0)
