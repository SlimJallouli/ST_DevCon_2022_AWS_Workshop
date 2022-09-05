import serial, serial.tools.list_ports
import sys


def get_name():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if "VID:PID=0483:374" in p.hwid:
            return 'stm32u5-' + p.serial_number[-10:]
    
    raise Exception("Port Error")

def main():
    device_id = get_name()
    print(device_id)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        sys.exit(1)