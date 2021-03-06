# Filename: image_backdrop.py
# Author: Zhiguo Wang
# Date: 11/7/2020
#
# Description:
# Transfer an image to the Host to use as the backdrop

import pylink
from PIL import Image

# Connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# Put the tracker in offline mode before we transfer the image
tk.setOfflineMode()

# convert an image to the <pixel> format supported by
# the bitmapBackdrop command
im = Image.open('sacrmeto.bmp')  # open an image with PIL
w, h = im.size  # get the width and height of an image
pixels = im.load()  # access the pixel data
pixels_img = [[pixels[i, j] for i in range(w)] for j in range(h)]

# Construct an image in <pixel> format with RGB tuples
white_rgb = (255, 255, 255)
black_rgb = (0, 0, 0)
pixels_rgb = [
    [black_rgb, black_rgb, black_rgb, white_rgb, white_rgb, white_rgb],
    [black_rgb, black_rgb, black_rgb, white_rgb, white_rgb, white_rgb],
    [black_rgb, black_rgb, black_rgb, white_rgb, white_rgb, white_rgb],
    [white_rgb, white_rgb, white_rgb, black_rgb, black_rgb, black_rgb],
    [white_rgb, white_rgb, white_rgb, black_rgb, black_rgb, black_rgb],
    [white_rgb, white_rgb, white_rgb, black_rgb, black_rgb, black_rgb],
    ]*100

# construct an image in <pixel> format with hexadecimal values alpha-R-G-B
white_hex = 0x00FFFFFF
black_hex = 0x0
pixels_hex = [
    [black_hex, black_hex, black_hex, white_hex, white_hex, white_hex],
    [black_hex, black_hex, black_hex, white_hex, white_hex, white_hex],
    [black_hex, black_hex, black_hex, white_hex, white_hex, white_hex],
    [white_hex, white_hex, white_hex, black_hex, black_hex, black_hex],
    [white_hex, white_hex, white_hex, black_hex, black_hex, black_hex],
    [white_hex, white_hex, white_hex, black_hex, black_hex, black_hex],
    ]*100

# Transfer the images to the Host PC screen
tk.sendCommand('clear_screen 0')
# tk.bitmapBackdrop(w, h, pixels_img, 0, 0, w, h,
#                  0, 0, pylink.BX_MAXCONTRAST)
tk.bitmapSaveAndBackdrop(w, h, pixels_img, 0, 0, w, h,
                         'trial_image', 'img', pylink.SV_MAKEPATH,
                         0, 0, pylink.BX_MAXCONTRAST)

# Show the image for 1-sec on the Host PC
pylink.msecDelay(3000)

# Transfer the checkerboard constructed with Hex values to the Host
# show it at (200,0) for 3-sec
tk.sendCommand('clear_screen 0')
tk.sendCommand('echo PIXELs_IN_HEX')
# tk.bitmapBackdrop(6, 6, pixels_hex, 0, 0, 6, 6,
#                  0, 0, pylink.BX_MAXCONTRAST)
tk.bitmapSaveAndBackdrop(6, 600, pixels_hex, 0, 0, 6, 600,
                         'trial_image', 'img', pylink.SV_MAKEPATH,
                         150, 0, pylink.BX_MAXCONTRAST)
pylink.msecDelay(3000)

# Transfer the checkerboard constructed with RGB tuples to the Host
# show it at (200, 0) for 3 sec
tk.sendCommand('clear_screen 0')
tk.sendCommand('echo PIXELs_IN_RGB')
# tk.bitmapBackdrop(6, 600, pixels_rgb, 0, 0, 6, 600,
#                  200, 0, pylink.BX_MAXCONTRAST)
tk.bitmapSaveAndBackdrop(6, 600, pixels_rgb, 0, 0, 6, 600,
                         'trial_image', 'img', pylink.SV_MAKEPATH,
                         200, 0, pylink.BX_MAXCONTRAST)
pylink.msecDelay(3000)

# Clear up the Host screen
tk.sendCommand('clear_screen 0')

# Close the connection
tk.close()
