#!/bin/zsh


# konsole --new-tab -e zsh -c "\

gnome-terminal --tab --title="python2.7-NAO" -x zsh -c "\
cd ~; \
####cd dir here
####source sdk here
####exec python here
exec zsh"



# launch the control panel
# konsole --new-tab -e zsh -c "\
gnome-terminal --tab --title="python3-YOLO" -x zsh -c "\
sleep 5; \
cd ~; \
####conda activate here
#### cd dir here
#### exec python here

exec zsh"
