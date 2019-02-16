# IMU_pi_logger

Logs Vectornav VN-200 IMU serial data on Raspberry Pi

## Usage
```
python IMU_logger.py
```

## Installation and Dependencies
To install logging, serial, and GPIO modules:
```
pip install logging
pip install pyserial
sudo apt-get install rpi.gpio
```

## Cron Reboot Scheduler
On bootup/restart, script will automatically run using Cron
```
sudo apt-get install gnome-schedule
```

To edit crontab:
```
crontab -e
```

Place this line inside to start the script on reboot or power cycle
```
@reboot python /home/pi/IMU_pi_logger/IMU_logger.py &
```
