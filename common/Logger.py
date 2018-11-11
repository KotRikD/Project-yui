import logging

"""Console colors"""
PINK = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

logging.basicConfig(format='[%(asctime)s] %(message)s',
                    filemode='at',
                    filename='projectyui.log',
                    level=logging.INFO)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


def printColored(string, color):
    logging.info("{}{}{}".format(color, string, ENDC))

def Ylog(msg):
    printColored(msg, PINK)

def Elog(msg):
    printColored(msg, RED)

def Nlog(msg):
    printColored(msg, YELLOW)

def Slog(msg):
    printColored(msg, GREEN)