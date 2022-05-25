import board, microcontroller
import busio, time, sys
import storage
import digitalio, sdcardio, pwmio
import os, array, math
from pycubed import cubesat
from micropython import const

time.sleep(5)  # Sleep so the board doesnt immediatly brick if something wrong


# This function listens for data continuously and logs the recieved data to
# a text file
def downlink_image():

    if cubesat.hardware['Radio1']:  # Check radio
        while True:
            packet = cubesat.radio1.receive()   # Listen for packet
            if packet is None:
                pass
            else:
                data_as_int = list(packet)  # Parse to list
                print(data_as_int)
                cubesat.log(data_as_int)    # Log data to text file
                rssi = cubesat.radio1.rssi  # Get signal strength
                print('Received signal strength: {0} dBm'.format(rssi))


while True:
    downlink_image()
    time.sleep(1)
    break
