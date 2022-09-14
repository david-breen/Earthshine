from skyfield.api import N, W, load, wgs84
from skyfield.trigonometry import position_angle_of
from skyfield.framelib import ecliptic_frame
import cv2 as cv
import math


def phase_ang(theta):
    f = ((math.pi() - math.abs(theta))*math.cos(theta))/math.pi()


ts = load.timescale()
t = ts.utc(2022, 6, 4, 22, 30)

eph = load('de421.bsp')
sun, moon, earth = eph['sun'], eph['moon'], eph['earth']
USM = earth + wgs84.latlon(43.681702 * N, 70.451827 * W)

b = USM.at(t)
m = b.observe(moon).apparent()
s = b.observe(sun).apparent()
print(position_angle_of(m.altaz(), s.altaz()))


e = earth.at(t)
_, slon, _ = e.observe(sun).apparent().frame_latlon(ecliptic_frame)
_, mlon, _ = e.observe(moon).apparent().frame_latlon(ecliptic_frame)
phase = ((mlon.degrees - slon.degrees) % 360.0)/180

print('{0:.3f}'.format(phase))

