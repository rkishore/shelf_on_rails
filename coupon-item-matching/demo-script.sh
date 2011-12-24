#!/bin/bash

# Display colorized information output
function cinfo() {
    COLOR='\033[01;33m' # bold yellow
    RESET='\033[00;00m' # normal white
    MESSAGE=${@:-"${RESET}Error: No message passed"}
    echo -e "${COLOR}${MESSAGE}${RESET}"
}
 
# Display colorized warning output
function cwarn() {
    COLOR='\033[01;31m' # bold red
    RESET='\033[00;00m' # normal white
    MESSAGE=${@:-"${RESET}Error: No message passed"}
    echo -e "${COLOR}${MESSAGE}${RESET}"
}

clear

cinfo "\nWelcome to dSense --- your friendly-neighborhood shopping guide"
cinfo "Enter your wishlist and let us tell you which brand to pick!\n" 
cinfo "\n------------- Express.com -------------------\n"

python match.py express

cinfo "\n------------- JCrew.com -------------------\n"

python match.py jcrew

cinfo "\nHope you liked us! Let us know!"