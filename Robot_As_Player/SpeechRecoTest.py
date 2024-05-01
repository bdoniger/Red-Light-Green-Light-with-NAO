'''
TEST RECO
'''

from naoqi import ALProxy
import time

# ip & port
nao_ip = "192.168.1.35"
nao_port = 9559

# connect
speechRecognition = ALProxy("ALSpeechRecognition", nao_ip, nao_port)

# set lan & word
speechRecognition.pause(True)
speechRecognition.setLanguage("English")
vocabulary = ["green", "red"]

speechRecognition.subscribe("ASR")
speechRecognition.unsubscribe("ASR")
speechRecognition.setVocabulary(vocabulary, False)



# while True:
for i in range(5):
    print("HERE",i)
    # get word
    speechRecognition.subscribe(nao_ip)
    
    memProxy = ALProxy("ALMemory", nao_ip, 9559)
    memProxy.subscribeToEvent('WordRecognized',nao_ip,'wordRecognized')

    speechRecognition.pause(False)
    time.sleep(5)

    speechRecognition.unsubscribe(nao_ip)
    words = memProxy.getData("WordRecognized")

    print( "word: %s" % words )
    print( "word type: %s" % type(words) )
    # words = speechRecognition.getRecognizedWordList()

    if "green" in words:
        print('HERE green')
    elif "red" in words:
        print('HERE red')
