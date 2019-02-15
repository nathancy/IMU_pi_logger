import logging
import serial
import os

class IMULogger(object):
    def __init__(self):
        self.initialize_logger_settings()
        self.initialize_IMU_serial_port()
        self.start()

        print(len('$VNACC,+00.105,-00.250,-10.148*4F'))

    def initialize_logger_settings(self):
        
        self.initialize_log_directory()
        logging.basicConfig(filename= self.path + self.filename, 
                            filemode='w', 
                            level=logging.INFO, 
                            format='%(asctime)s,%(message)s', 
                            datefmt='%d-%b-%y,%H:%M:%S')
        logging.info('Successfully loaded logger configuration settings')
        
        exit(1)
    def initialize_IMU_serial_port(self):
        self.ser = serial.Serial('/dev/ttyUSB0')
        self.ser.baudrate = 230400

    def initialize_log_directory(self):
        self.path = '/home/pi/IMU_pi_logger/logs/'

        if not os.path.exists(self.path):
            os.makedirs(self.path)
            self.filename = 'IMU0000.log'
        else:
            self.filename = self.get_next_log_file_name()

    def get_next_log_file_name(self):
        def extract_digits(filename):
            s = ''
            for char in filename:
                if char.isdigit():
                    s += char
            return int(s)

        l = [extract_digits(filename) for filename in os.listdir(self.path)]
        latest_file_number = max(l)
        self.filename = 'IMU' + '{0:04d}'.format(latest_file_number + 1) + '.log'
        return self.filename
                    
    def start(self):
        while True:
            s = self.ser.readline()
            print(s)
            print(len(s))
            

if __name__ == '__main__':
    logger = IMULogger()
