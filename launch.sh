#!/bin/sh

use_venv="y"
if [[ -f ./biogascontrollerapp/.venv/bin/activate ]]; then
    if [[ "$SHELL" == "fish" ]]; then
        source ./.venv/bin/activate.fish
    elif [[ "$SHELL" == "csh" ]]; then
        source ./.venv/bin/activate.csh
    else
        source ./.venv/bin/activate
    fi
        
    if [[ !command -v deactivate >/dev/null 2>&1 ]]; then
        echo "Virtual environment could not be activated. Trying to run anyway"
    fi
fi

cd ./biogascontrollerapp/
python biogascontrollerapp.py
