import logging
import serial
import os
import RPi.GPIO as GPIO
import time

class IMULogger(object):
    """Logs Vectornav VN-200 IMU serial data"""

    def __init__(self):
        self.initialize_logger_settings()
        self.initialize_IMU_serial_port()
        self.initialize_LED()
        self.start()

    def initialize_logger_settings(self):
        """Set logger configuration settings"""
        
        self.initialize_log_directory()
        logging.basicConfig(filename= self.path + self.filename, 
                            filemode='w', 
                            level=logging.INFO, 
                            format='%(asctime)s.%(msecs)03d,%(message)s',
                            datefmt='%d-%b-%y,%H:%M:%S')
        logging.info('Successfully loaded logger configuration settings')
        self.status = True

    def initialize_LED(self):
        """Set GPIO settings"""

        self.LED_PIN = 40
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.LED_PIN, GPIO.OUT, initial=GPIO.LOW)
        
    def initialize_IMU_serial_port(self):
        """Connect to IMU serial port"""

        self.ser = serial.Serial('/dev/ttyUSB0')
        self.ser.baudrate = 230400

    def initialize_log_directory(self):
        """Create IMU directory and IMU file"""

        self.path = '/home/pi/IMU_pi_logger/logs/'

        if not os.path.exists(self.path):
            os.makedirs(self.path)
            self.filename = 'IMU0000.log'
        else:
            self.filename = self.get_next_log_file_name()

    def get_next_log_file_name(self):
        """Scans log directory for latest log file and returns a new filename"""

        def extract_digits(filename):
            s = ''
            for char in filename:
                if char.isdigit():
                    s += char
            return int(s)
        
        l = [extract_digits(filename) for filename in os.listdir(self.path)]
        # Directory is empty
        if not l:
            return 'IMU0000.log'
        # Directory has files so find latest
        else:
            latest_file_number = max(l)
            return 'IMU' + '{0:04d}'.format(latest_file_number + 1) + '.log'
                    
    def start(self):
        """Set status LED and start logger"""

        try:
            GPIO.output(self.LED_PIN, GPIO.HIGH)
            while True:
                data = self.ser.readline().rstrip()
                if data[:6] == '$VNACC' and len(data) == 33:
                    logging.info(data)
        except KeyboardInterrupt:
            logging.info('ERROR: KeyboardInterrupt')
        except Exception as e:
            logging.info('ERROR: ' + str(e))
        finally:
            logging.info('Cleanup')
            GPIO.cleanup()
            
if __name__ == '__main__':
    logger = IMULogger()
