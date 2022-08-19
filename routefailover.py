import firepower
from pythonping import ping
import sys
from time import sleep
import json
from pathlib import Path

####### Option load:
optionFile = Path(__file__).parent / './options.json'
with open(optionFile, "rb") as opt:
    options = json.load(opt)['pingtest']
DEFAULT_DESTINATION = options['target']
PING_COUNT = options['count']
MAX_LATENCY = options['max_latency']
MAX_LOSS = options['max_loss']
#######

