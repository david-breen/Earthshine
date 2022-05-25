# Earthshine
This is a repository for code pertaining to the Earthshine cubesat project at USM

Currently all of the current code for the project is placed in this repository, however it will probably migrate to 3 or more repositries soon

# Groundstation
Basic functionality for recieving images from the transmit side of the pycubed
## Recieve

## Image Constrction
  This directory contains scripts for re-assembling an image once it has been transmitted to the ground station. This is necessary as the images are transmitted broken up into packets.
  
 1. Octave
    * This script needs some manual labor to get working, however it shows the concepts of what can be done to reassemble the imace
    * The files need a beter method of deliniation or handeling missing packets

# Satellite
Basic functionality for sending images from the pycubed


# Earthshine Measurement

The earthshine measurement folder contains 3 main components as of yet. 

1. A python script that takes in a folder of images, reads them and produces an HDR image
2. A folder of images to be read by the above python script
3. An openMV program for taking a single series of images 
