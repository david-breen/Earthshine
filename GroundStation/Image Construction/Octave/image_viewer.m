clc
clear
close all
% This script takes in a text file filled with data from the camera
% and generates an image with it

image_width = 320;   % width of the expected image
image_height = 240;  % height of the expected image

B = zeros(image_height, image_width); % Generate matrix to store the pixels

[A] = dlmread( 'log1.txt', ',');  % Read the text file containing the pixels

q = zeros(7,100); % add the missing rows of data

A = [A;q];   

s = reshape(A',100*4,240)';

image(s,'CDataMapping','scaled'); % Display the image
colorbar;