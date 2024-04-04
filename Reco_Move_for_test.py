'''
Reco DONE
Move DONE
'''

from naoqi import ALProxy
import time

# ip & port
nao_ip = "192.168.1.35"
nao_port = 9559

motion = ALProxy("ALMotion", "192.168.1.35", 9559)
bodyPart = "Body"
stiffness = 1.0
timeDuration = 10
motion.stiffnessInterpolation(bodyPart, stiffness, timeDuration)
motion.moveInit()

# connect
speechRecognition = ALProxy("ALSpeechRecognition", nao_ip, nao_port)

# set lan & word
speechRecognition.pause(True)
speechRecognition.setLanguage("English")
vocabulary = ["green", "red"]

speechRecognition.subscribe("ASR")
speechRecognition.unsubscribe("ASR")
speechRecognition.setVocabulary(vocabulary, False)

motion = ALProxy("ALMotion", "192.168.1.35", 9559)

# while True:
for i in range(5):
    print("HERE",i)
    # get word
    speechRecognition.subscribe(nao_ip)
    
    memProxy = ALProxy("ALMemory", nao_ip, 9559)
    memProxy.subscribeToEvent('WordRecognized',nao_ip,'wordRecognized')

    speechRecognition.pause(False)
    time.sleep(8)

    speechRecognition.unsubscribe(nao_ip)
    words = memProxy.getData("WordRecognized")

    print( "word: %s" % words )
    print( "word type: %s" % type(words) )
    # words = speechRecognition.getRecognizedWordList()

    if "green" in words:
        print('HERE green')

        # motion = ALProxy("ALMotion", "192.168.1.35", 9559)
        # motion.setStiffnesses("Legs", 1.0)
        # motion.moveInit()

        # reduce distance
        # add wait
        motion.post.moveTo(0.0002, 0.0, 0.0)
        time.sleep(2)

        motion.post.moveTo(0.0002, 0.0, 0.0)
        time.sleep(2)

        motion.post.moveTo(0.0002, 0.0, 0.0)
        time.sleep(2)

        motion.post.moveTo(0.0002, 0.0, 0.0)
        
    elif "red" in words:
        print('HERE red')
        # motion = ALProxy("ALMotion", "192.168.1.35", 9559)
        # motion.setStiffnesses("Legs", 1.0)
        # motion.moveInit()
        
        # NEED TO CONFIRM
        motion.stopMove()  
        motion.post.moveTo(0.0, 0.0, 0.0)

        # lower speed
        # init motion before loop
