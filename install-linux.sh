#!/bin/sh

# Create virtual environment to not clutter up local python install
echo "

 ___                            ___               _              _   _              _____             
(  _ \ _                       (  _ \            ( )_           (_ )(_ )           (  _  )            
| (_) )_)  _     __    _ _  ___| ( (_)  _    ___ |  _)_ __   _   | | | |   __  _ __| (_) |_ _   _ _   
|  _ (| |/ _ \ / _  \/ _  )  __) |  _ / _ \/  _  \ | (  __)/ _ \ | | | | / __ \  __)  _  )  _ \(  _ \ 
| (_) ) | (_) ) (_) | (_| |__  \ (_( ) (_) ) ( ) | |_| |  ( (_) )| | | |(  ___/ |  | | | | (_) ) (_) )
(____/(_)\___/ \__  |\__ _)____/____/ \___/(_) (_)\__)_)   \___/(___)___)\____)_)  (_) (_)  __/|  __/ 
              ( )_) |                                                                    | |   | |    
               \___/                                                                     (_)   (_)    


        WELCOME! This script will automatically install BiogasControllerApp for you!

        We first have to ask a few questions. If you are unsure what they mean,
        simply press enter to use default options, which are designed to make 
        uninstalling much easier. The default option is highlighted using capital
        letters.

        Please ensure you have wget installed. The script will verify and tell you
        if you do not have it installed

        If this script is not inside a full copy of the BiogasControllerApp repo,
        the repo will be automatically downloaded for you.
"

use_venv=""
read -p "Install dependencies in a virtual environment? (Y/n) " use_venv
use_venv=$(echo "$use_venv" | tr '[:upper:]' '[:lower:]')

echo "\n => Checking for repo..."

if [[ -f ./biogascontrollerapp.py ]]; then
    echo "\n  -> Data found, not downloading"
else
    do_download=""
    read -p "  -> Data not found, okay to download? (Y/n) " do_download
    do_download=$(echo "$do_download" | tr '[:upper:]' '[:lower:]')
    if [[ "$do_download" == "y" || "$do_download" == "" ]]; then
        # Check if wget is installed
        if [[ !command -v wget >/dev/null 2>&1 ]]; then
            echo "wget unavailable. Please install using your distribution's package manager or manually download the repo from GitHub releases"
            echo 1
        fi

        # Download the latest release package
        wget https://github.com/janishutz/BiogasControllerApp/releases/latest/download/biogascontrollerapp-linux.tar.gz

        # Extract the tar (as tar is basically standard on all distros)
        tar -xf ./biogascontrollerapp-linux.tar.gz

        # Remove tarball (to keep it clean)
        rm ./biogascontrollerapp.tar.gz

        cd biogascontrollerapp/
    else
        echo "Please download the repo manually and execute the script inside the downloaded repo from GitHub releases"
        exit 1
    fi
fi

# We are now guaranteed to be in the base directory of the repo
# Set up venv if selected
if [[ "$use_venv" == "y" || "$use_venv" == "" ]]; then
    python -m venv .venv
    if [[ "$SHELL" == "fish" ]]; then
        source ./.venv/bin/activate.fish
    elif [[ "$SHELL" == "csh" ]]; then
        source ./.venv/bin/activate.csh
    else
        source ./.venv/bin/activate
    fi
        
    if [[ !command -v deactivate >/dev/null 2>&1 ]]; then
        echo "Virtual environment could not be activated.
        You may install the dependencies by changing to the biogascontrollerapp directory and running
        pip install -r requirements.txt"
        exit 1
    fi
fi

pip install -r requirements.txt


echo "
  ==> Installation complete!
"
