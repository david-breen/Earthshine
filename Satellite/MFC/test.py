import time
import board
import busio
import digitalio
from pycubed import cubesat


time.sleep(5)
cubesat.spi.deinit()
cs = digitalio.DigitalInOut(board.PB17)
cs.direction = digitalio.Direction.OUTPUT
cs.value = True

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
spi.configure(baudrate=5000000, phase=0, polarity=0)

buffer1 = bytearray([0xDE. 0xAD, 0xBE, 0xEF])


while True:

    while not spi.try_lock():
        pass

    spi.unlock()



    cs.value = False
    spi.write(buffer1)
    result = bytearray(4)
    spi.readinto(result)
    cs.value = True
    print(result)
    result
    bytearray(b'\x01\xa8\x1a\xf0')
