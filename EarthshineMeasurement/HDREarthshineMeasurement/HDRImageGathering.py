from os import listdir
from os.path import isfile, join
import math
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# This script serves two purposes
# The first of which is to reture a calibration response curve
# for an image sensor based on a set of images
# The second is to generate an HDR dataset and image


# Load all file names from the Test images folder
img_fn = ["TestImages/" + f for f in listdir("TestImages")
          if isfile(join("TestImages", f))]


# If you would like to add the images manualy you may add them here
"""
img_fn = ["TestImages/image1.bmp",
          "TestImages/image2.bmp",
          "TestImages/image3.bmp",
          "TestImages/image4.bmp",
          "TestImages/image5.bmp"]
"""

img_list = [cv.imread(fn) for fn in img_fn]

# This is where you add the exposure times
exposure_times = np.array([1e-6*math.pow(2, 8),
                           1e-6*math.pow(2, 9),
                           1e-6*math.pow(2, 10),
                           1e-6*math.pow(2, 11),
                           1e-6*math.pow(2, 12),
                           1e-6*math.pow(2, 13),
                           1e-6*math.pow(2, 14),
                           1e-6*math.pow(2, 15)], dtype=np.float32)
pixel_values = np.arange(0, 256, 1)

# Merge exposures to HDR image
merge_debevec = cv.createMergeDebevec()
hdr_debevec = merge_debevec.process(img_list, times=exposure_times.copy())

sensor_calibration = cv.createCalibrateDebevec()

# SetRandom=True allows the calibration to select random points around image
# SetSamples is the number of samples that calibration will take around image
sensor_calibration.setRandom(True)
sensor_calibration.setSamples(250)

response_curve = sensor_calibration.process(img_list,
                                            times=exposure_times.copy())

# Tonemap HDR image
tonemap1 = cv.createTonemap(gamma=2.2)
res_debevec = tonemap1.process(hdr_debevec.copy())

# Exposure fusion using Mertens
merge_mertens = cv.createMergeMertens()
res_mertens = merge_mertens.process(img_list)

# If you would like to generate an 8 bit image
# with the data uncomment these two lines
res_debevec_8bit = np.clip(res_debevec*255, 0, 255).astype('uint8')
cv.imwrite("ldr_debevec.jpg", res_debevec_8bit)


fig, rCurve = plt.subplots()  # Create a figure containing a single axes
rCurve.plot(pixel_values, response_curve[:, 0, 0])  # Plot some data
rCurve.set_ylabel("Calibrated Intensity Value (Relative Irradiance)")
rCurve.set_xlabel("Pixel Value")
plt.show()
