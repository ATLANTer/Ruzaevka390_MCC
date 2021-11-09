import sys
import glob
import serial
import csv


def serial_ports():
    """ Lists serial port names
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def csv_writer(delimiter, header, file_path, data):
    writefile = open(file_path, 'w', newline='')
    data.append(header)
    data.reverse()
    writer = csv.writer(writefile, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i in data:
        writer.writerow(i.split(';')[:-1])
    writefile.close()


def main():
    print(serial_ports())


if __name__ == "__main__":
    main()
