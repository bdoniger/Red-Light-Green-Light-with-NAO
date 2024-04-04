from naoqi import ALProxy
import time

nao_ip = "192.168.1.35"
nao_port = 9559

motion = ALProxy("ALMotion", nao_ip, nao_port)
motion.wakeUp()

posture = ALProxy('ALRobotPosture', nao_ip, nao_port)
posture.goToPosture("Stand", 1.0)
