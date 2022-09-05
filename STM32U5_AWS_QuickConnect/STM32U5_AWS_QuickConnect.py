from ast import Interactive
import sys
import subprocess
from tokenize import Name
from utils.getDeviceName import *
import getopt
import getpass

SSID = 'ssid'
PSWD = 'pswd'
DUMMY_SSID = '0'
DUMMY_PSWD = '0'
BIN_FILE = '..\\Projects\\b_u585i_iot02a_ntz\\Debug\\b_u585i_iot02a_ntz.bin'
VERSION="1.0.0"

HELP = ['openDashboard.py options:', 
        '\n\t-h or --help for help',
        '\n\t-i for interactive mode',
        '\n\t--version for file version',
        '\n\t--ssid=[WiFi SSID]', 
        '\n\t--password=[WiFi Password]']

# Run path in command line and output it to output.txt if logging level is greater than debug
def cmd(path: list):
    proc = subprocess.Popen(path)
    proc.communicate()
    retState = proc.poll()

    if retState != 0:
        print('Error: ' + path[1])
        sys.exit(1)


def getParam(curParam, label):
    param = input(label + " [" + curParam + "]: ").strip()

    if param:
        return param
    else:
        return curParam

def getHiddenParam(curParam, label):
    hidden = '*' * len(curParam)
    param = getpass.getpass(prompt=label + " [" + hidden + "]: ").strip()

    if param:
        return param
    else:
        return curParam


def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hi", ["help", "interactive", "version", "ssid=", "password=", "key=", "secret-key="])
    except getopt.GetoptError:
        print("Parameter Error")
        sys.exit(1)

    name = get_name()
    ssid = SSID
    pswd = PSWD
    interactiveMode = False


    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(*HELP)
            sys.exit(1)
        
        elif opt in ("--version"):
            print("STM32U5_AWS_QuickConnect.py version: " +VERSION)
            sys.exit(1)

        elif opt in ("--ssid"):
            ssid  = arg

        elif opt in ("--password"):
            pswd = arg

        elif opt in ("-i", "--interactive"):
            interactiveMode = True


    if interactiveMode:
        ssid = getParam(ssid, "Wi-Fi SSID")
        pswd = getHiddenParam(pswd, "Wi-Fi Password")

    
    cmd(['python', 'utils\\flash.py', '--bin-file='+BIN_FILE])
    cmd(['python', 'utils\\setWiFiParam.py', '--ssid=' + DUMMY_SSID, '--password='+ DUMMY_PSWD])
    cmd(['python', 'utils\\provision.py', '--thing-name=' + name, '--wifi-ssid=' +  ssid, '--wifi-credential=' + pswd])
    cmd(['python', 'utils\\readSerial.py'])

if __name__ == "__main__":
    main(sys.argv[1:])