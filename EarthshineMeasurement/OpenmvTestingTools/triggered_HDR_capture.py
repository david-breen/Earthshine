import sensor, image, time, pyb, math

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # Set pixel format to GRAYSCALE
sensor.set_framesize(sensor.WVGA)    # Set frame size to VGA (640x480)
sensor.set_windowing(200,200)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.
sensor.set_auto_gain(False)



# Note: OpenMV Cam runs about half as fast when connected
# to the IDE. The FPS should increase once disconnected.

# This script will take a series of images with the camera at pre defined exposure intervals
# The exposure times can be set below, by adding values to the eposure array

# The camera will take a series of images once per run

# Exposure values are in microseconds

exposures = [math.pow(2,8),
             math.pow(2,9),
             math.pow(2,10),
             math.pow(2,11),
             math.pow(2,12),
             math.pow(2,13),
             math.pow(2,14),
             math.pow(2,15),
             math.pow(2,16),
             math.pow(2,17),
             math.pow(2,18),
             math.pow(2,19)]  # Last value truncates to .5s (Longst exposure time?)

file_format = "image1262020_%2d_Test.bmp" % (exposure_time)

# Setting the camera to triggered snapshot mode (NON VIDEO)
sensor.ioctl(sensor.IOCTL_SET_TRIGGERED_MODE, True)

def init_sensor():

    sensor.reset()
    sensor.set_pixformat(sensor.GRAYSCALE) # grayscale is faster
    sensor.set_framesize(sensor.VGA)      # full resolution is vga
    sensor.skip_frames(time = 2000)

def sensor_settings(current_exposure_time_in_microseconds):

    sensor.set_auto_exposure(False, \
        exposure_us = int(current_exposure_time_in_microseconds))

    #Change the gain for the camera sensor here Max is 32 min is 1? 0? -1?
    current_gain_in_decibels = 1

    sensor.set_auto_gain(False, \
        gain_db = current_gain_in_decibels)

def capture_image(exposure_time, file_name):

    pyb.LED(1).on()

    # Set the file name here

    sensor.snapshot().save(file_name)
    print(sensor.get_exposure_us())
    sensor.flush()  # Might not need this

    pyb.LED(1).off()


init_sensor()

for frameTime in exposures:
    sensor_settings(frameTime)
    capture_image(frameTime, file_format)




