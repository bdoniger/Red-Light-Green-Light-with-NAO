# Stop n Go with Nao

This is the code designed to be enable a NAO robot to play the game "Red Light, Green Light." This project is the final project for CS 4501 (Human-Robot Interaction) at UVA. 

Members of this team are: Cooper Wang, Yixuan Ren, Jiahui Zhang, and Ben Doniger. The professor for this course was Professor Tariq Iqbal. 

## 1. Branches

```.
├── main
├── test
├── bot_as_leader
└── bot_as_player
```

1. Please do not directly push to main
2. Create a branch or checkout to subbranches like `bot_as_leader`
3. Add changes and commit them
4. Fetch and merge into main (when section finished)
5. Resolve any merge issues
6. Create a pull request to merge into main

## 2. Environment

1. **NAO development requirement**

   1. python = 2.7
   2. naoqi python SDK
   3. multiprocessing package
2. **Detection requirement**

   1. python >= 3.8
   2. conda env
   3. pytorch
   4. ```bash
      conda activate <your_env>
      cd /path/to/detection
      pip install -r requirement.txt
      ```
   Check if you install pytorch properly. Otherwise, modify the code to disable cuda.
## 3. Communication Bridge
I take advantage of sockets (and named pipe on windows) to established a conncection on localhost. 
Any data less than 32MB (once) could be transmit through the bridge to communicate py2 and py3 threads.
I hack the `multiprocessing` lib a little bit, overriding the `send()` function, to avoid `pickle` version problem.  
## 4. Dectection
1. **Modules**
   1. Opencv `cv2`
   2. yolov8 `Yolo` 
