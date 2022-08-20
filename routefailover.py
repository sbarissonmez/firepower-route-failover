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


def doPing():
    # Run ping against target destination
    try:
        print("Checking loss/latency to " + DEFAULT_DESTINATION)
        result = ping(DEFAULT_DESTINATION, size=2, count=PING_COUNT,
                      verbose=True)
    except PermissionError:
        # must have privileges to ping
        print("Error: User not root! Cannot open socket")
        sys.exit(0)
    sleep(1)
    print("Calculating results...")
    loss = calculateLoss(result)
    print("AVG response time: " + str(result.rtt_avg_ms) +
          "ms. Loss = " + str(loss) + "%")
    print("Target response time: <" + str(MAX_LATENCY) +
          "ms. Target Loss: <" + str(MAX_LOSS))
    return result.rtt_avg_ms, loss
