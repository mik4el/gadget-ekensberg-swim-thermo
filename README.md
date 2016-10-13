# gadget-ekensberg-swim-thermo
Everything for building and getting the gadget Ekensberg Swim Thermometer to run.

## Dependencies
1. requests 
1. pyserial
1. python3
1. Docker, Docker-compose

## Install with docker
1. Copy `.env` from `.env.sample` and fill out 
1. `docker-compose up`

## Install without docker
On local:

1. `scp post_serial_data.py pi@10.0.0.4:.`

On pi:

1. `curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash`
1. `sudo nano ~/.bashrc` according to https://github.com/yyuu/pyenv-installer
1. `pyenv install 3.5.1`
1. `pip install pyserial`
1. `pip install requests`

### Run
1. Copy script to pi
1. Install deps on pi
1. Run it in e.g. byobu

### Testing
1. Run `python -m unittest tests`
