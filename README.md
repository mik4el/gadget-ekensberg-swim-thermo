# gadget-ekensberg-swim-thermo
Everything for building and getting the gadget Ekensberg Swim Thermometer running.

## Install
On local:
1. scp post_serial_data.py pi@10.0.0.4:.

On pi:
1. `curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash`
1. `sudo nano ~/.bashrc` according to https://github.com/yyuu/pyenv-installer
1. `pyenv install 3.5.1`
1. `pip install pyserial`
1. `pip install requests`

## Run
1. Copy script to pi
1. Install deps on pi
1. Run it in e.g. byobu

## Testing
1. Run `python -m unittest tests`

## Dependencies
requests, pyserial, py2.7

## Todo 
1. Dockerize raspi
1. Dockerize script
1. Serious logging