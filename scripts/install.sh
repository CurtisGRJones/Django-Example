#! /bin/bash

echo "Intalling..."

INSTALL_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
echo "Using $INSTALL_DIR"

echo "Installing Dependencies"

if ! command -v python3.11 &> /dev/null
then
    echo "Python version 3.11 not found, installing"
    sudo apt install python3.11
    sudo apt install python3.11-venv
fi


PYTHON_VENV_PATH="$INSTALL_DIR/../.venv"
echo "Createing venv at $PYTHON_VENV_PATH"

python3.11 -m venv $PYTHON_VENV_PATH &> /dev/null

echo "Sourcing venv"
source "$PYTHON_VENV_PATH/bin/activate"

echo "Installing pip requirements"

pip install -r "$INSTALL_DIR/pip/requirements.txt"

deactivate

