import board, microcontroller
import busio, time, sys
import storage
import digitalio, sdcardio, pwmio
import os, array, math
from pycubed import cubesat
from micropython import const

time.sleep(5)

handshake_byte = bytearray([0,1,2,3,4,5,6,7])

i2c2 = busio.I2C(board.SCL2, board.SDA2)


def ping_camera(addr):
    rec_flag = False

    read_buffer = bytearray(8)

    print('waiting for camera')
    while not rec_flag:
        if i2c2.try_lock():
            for address in i2c2.scan():
                if address == addr:
                    print('sending handshake')
                    try:
                        i2c2.writeto(addr, handshake_byte)
                    except OSError as error:
                        pass
                    time.sleep(.05)
                    try:
                        i2c2.readfrom_into(addr, read_buffer)
                    except OSError as error:
                        pass

                    if read_buffer == bytearray([9,8,7,6,5,4,3,2]):
                        rec_flag = True
                        print(read_buffer)

                else:
                    pass

            i2c2.unlock()



def recieve_image(addr):


    rec_flag = False
    img = array.array('b',[0]*320)

    print('awaiting data')
    while not rec_flag:

        if i2c2.try_lock():

            try:
                i2c2.readfrom_into(addr, img)
            except OSError as error:
                pass

            #if (img[100] > 0 |img[2] > 0 | img[200] > 0):
            rec_flag = True
            #time.sleep(0.01)
            try:
                i2c2.writeto(addr, handshake_byte)
            except OSError as error:
                pass
            print('data recieved')

            i2c2.unlock()
    return img


def send_line(line):
    count = len(line)
    print(count)

    k = 100
    n = math.ceil(count/k)
    start = 0
    end = 0

    if cubesat.hardware['Radio1']:
        for pk in range(n):
            end = start+k
            packet = bytearray(line[start:end])
            #print(packet)
            cubesat.radio1.send(packet)
            start = end
            time.sleep(.1)


while True:

    ping_camera(0x42)
    for i in range(240):
        send_line(recieve_image(0x42))
        time.sleep(.01)
    time.sleep(1)

    break










    # Write your code here :-)
