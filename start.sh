#!/bin/zsh



#konsole --new-tab -e zsh -c "\
gnome-terminal --tab --title="python2.7-NAO" -x zsh -c "\
cd /home/cooper/Desktop/HRI_project/nao_project/nao; \
source /home/cooper/anaconda3/bin/activate HRI_project;\
python fake_nao_main.py; \
exec zsh"



# launch the control panel
#konsole --new-tab -e zsh -c "\
gnome-terminal --tab --title="python3-YOLO" -x zsh -c "\
source /home/cooper/anaconda3/bin/activate HRI_project_yolo;\
cd /home/cooper/Desktop/HRI_project/nao_project/detection; \
python detection_main.py; 
exec zsh"\
