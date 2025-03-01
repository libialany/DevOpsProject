#!/bin/bash

ugc() {
    sudo apt update && sudo apt --only-upgrade install google-chrome-stable
}
ugc1(){
    wget http://dl.google.com/linux/chrome/deb/ && sudo dpkg -i google-chrome-stable_current_amd64.deb
}
