# Find Circles Example
#
# This example shows off how to find circles in the image using the Hough
# Transform. https://en.wikipedia.org/wiki/Circle_Hough_Transform
#
# Note that the find_circles() method will only find circles which are completely
# inside of the image. Circles which go outside of the image/roi are ignored...

import sensor, image, time, rpc
import pyb
from pyb import Pin, I2C
GAIN_SCALE = 1.0
EXPOSURE_TIME_SCALE = 1.0


#sensor.set_auto_whitebal(False)
clock = time.clock()

shutter_button = Pin('P6', Pin.IN, Pin.PULL_UP)
scl = Pin('P4',Pin.IN,Pin.PULL_NONE)
sda = Pin('P5',Pin.IN,Pin.PULL_NONE)

i2c = I2C(2)
i2c = I2C(2, I2C.MASTER)
i2c.deinit()
i2c.init(I2C.SLAVE, addr=0x42)

current_exposure_time_in_microseconds = 5000000

recv_flag = False

buffer_test1=bytearray([9,8,7,6,5,4,3,2])



def handshake_i2c():

    print('Waiting handshake')
    recv_flag = False
    buffer_test=[]
    while not recv_flag:

        try:
            buffer_test = i2c.recv(8,timeout = 5000)
        except OSError as error:
            pass

        print(buffer_test)

#######################################################

        if buffer_test == bytearray([0,1,2,3,4,5,6,7]):

            try:
                i2c.send(buffer_test1,timeout=5000)
            except OSError as error:
                pass
                print('send failed')

            recv_flag = True
            print('Hand is Shook')
        else:
            recv_flag = False

    return recv_flag


def transfer_image_i2c(img):

    rec_flag = False


    while not rec_flag:
        print('sending')
        time.sleep_ms(10)
        try:
            i2c.send(img,timeout=51000)
        except OSError as error:
                pass
                print('send failed')
        try:
            if i2c.recv(8,timeout=5000)==bytearray([0,1,2,3,4,5,6,7]):
                rec_flag = True
        except OSError as error:
            pass

def transfer_image_size():

    try:
        i2c.send(img.height(), timeout=5000)
        i2c.send(img.width(), timeout=5000)
    except OSError as error:
        pass
        print('send failed')



def init_sensor():

    sensor.reset()
    sensor.set_pixformat(sensor.GRAYSCALE) # grayscale is faster
    sensor.set_framesize(sensor.QVGA)
    sensor.skip_frames(time = 2000)


def sensor_settings():

    sensor.set_auto_exposure(False, \
        exposure_us = int(current_exposure_time_in_microseconds * EXPOSURE_TIME_SCALE))

    current_gain_in_decibels = 128

    sensor.set_auto_gain(False, \
        gain_db = current_gain_in_decibels * GAIN_SCALE)


def capture_image():

    img = sensor.snapshot()
    print(1)

    for c in img.find_circles(threshold = 2000, x_margin = 200, y_margin = 200, r_margin = 100,
                              r_min = 15, r_max = 50, r_step = 10):
        img.draw_circle(c.x(), c.y(), 15, color = (255, 0, 0))
        img.draw_circle(c.x(), c.y(), 50, color = (255, 0, 0))
    return img


def get_image_row(row, img):

    buffer = bytearray()
    wide = img.width()

    for i in range(wide):
       buffer.append(img.get_pixel(i,row))


    return buffer


def callback(line):
    print(line)
    try:
        transfer_image_spi(img)
    except OSError as err:
        pass


init_sensor()

while(True):
    clock.tick()
    img = capture_image()
    print(len(img.bytearray()))
    print(img.height())
    print(img.width())
    print(img.get_pixel(2,2))
    print(len(get_image_row(1,img)))


    handshake_i2c()
    for row in range(img.height()):
        print(row)
        transfer_image_i2c(get_image_row(row,img))
        time.sleep_ms(100)

    time.sleep_ms(1000)



















