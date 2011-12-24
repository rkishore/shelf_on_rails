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

python match.py ../shopstyle-int/express-mens-shirts-ss.data ../shopstyle-int/express-mens-pants-ss.data ../shopstyle-int/express-mens-jeans-ss.data ../shopstyle-int/express-womens-jeans-ss.data ../shopstyle-int/express-womens-sweaters-ss.data express_dec_22 

cinfo "\n------------- JCrew.com -------------------\n"

python match.py ../shopstyle-int/jcrew-mens-shirts-ss.data ../shopstyle-int/jcrew-mens-pants-ss.data ../shopstyle-int/jcrew-mens-jeans-ss.data ../shopstyle-int/jcrew-womens-jeans-ss.data ../shopstyle-int/jcrew-womens-sweaters-ss.data jcrew_dec_18

cinfo "\nHope you liked us! Let us know!"