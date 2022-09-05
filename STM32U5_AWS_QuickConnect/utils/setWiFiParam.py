from mimetypes import common_types
import serial, serial.tools.list_ports
import time
import getopt, sys


HELP = ['openDashboard.py options:', 
        '\n\t-h or --help for help',
        '\n\t--ssid=[WiFi SSID]', 
        '\n\t--password=[WiFi Password]']

def get_com():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if "VID:PID=0483:374" in p.hwid:
            return p.device
    
    return " PORT ERR "


def set_param(com, key, value, ser):
    #print('conf set ' + key + ' ' + value)
    ser.write(bytes('conf set ' + key + ' ' + value + '\r\n', 'utf-8'))
    time.sleep(0.1)
    
def commit(ser):
    ser.write(bytes('conf commit\r\n', 'utf-8'))
    time.sleep(0.5)

def reset(ser):
    ser.write(bytes('reset\r\n', 'utf-8'))
    time.sleep(2)


def main(argv):
    Commit = False
    try:
        opts, args = getopt.getopt(argv,"h", ["help", "ssid=", "password="])
    except getopt.GetoptError:
        print("Parameter Error")
        sys.exit(1)

    com = get_com()

    try:
        ser = serial.Serial(com, 115200)
    except  Exception:  
        print("\r\nCould not open serial port\r\n")
        sys.exit(1)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(*HELP)
            sys.exit(1)

        elif opt in ("--ssid"):
            print("Setting Wi-Fi SSID")
            set_param(com, 'wifi_ssid', arg, ser)
            Commit = True

        elif opt in ("--password"):
            print("Setting Wi-Fi Password")
            set_param(com, 'wifi_credential', arg, ser)
            Commit = True

    if (Commit == True):
        print("Commit changes")
        commit(ser)
        print("Device reset")
        reset(ser)
    
    ser.close()

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as e:
        print(e)
        sys.exit(-1)