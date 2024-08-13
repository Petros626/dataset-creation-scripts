######## PiCamera2 picture taker for the RPI IR-Cut camera #########

# Author: Petros626
# forked from/oriented on: https://github.com/EdjeElectronics/Image-Dataset-Tools/blob/main/PictureTaker/PictureTaker.py
# Date: 28.02.2023
# Description: 
# This program takes pictures (.png format - 95% quality and 0 compression) from a the RPi IR-Cut 
# camera and saves them in the specified directory. The default directory is 'images' and the
# default resolution is 1920x1080.

# Example usage to save images in a directory named images at 1920x1080 resolution:
# python3 run_camera_config.py --imgdir=images --res=1920x1080

# This code is based off the Picamera2 library examples at:
# https://github.com/raspberrypi/picamera2/tree/a9f7a7d0bac726ab9b3f366ff461ddd62e885f40/examples 

from picamera2 import Picamera2, Preview
from os import getcwd, path, makedirs
from argparse import ArgumentParser
from keyboard import is_pressed
from termios import tcflush, TCIOFLUSH
from sys import stdin, exit
from libcamera import controls

# If you get "Could not load the Qt platform plugin "xcb"after import OpenCV"
# fix 1: use os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")
# fix 2: try pip install opencv-python-headless (without GUI)
# fix 3: delete the libqxcb from  "/home/pk/.local/lib/python3.9/site-packages/cv2/qt/plugins/platforms
#os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")

#### Parser and safety requests #####
# Fetch script arguments
parser = ArgumentParser()
parser.add_argument("--imgdir", help = "Folder where the taken images get saved. If you not specify there will be created one automatically.",
                    default = "images")
parser.add_argument("--res", help = "Required resolution in WxH. To avoid erros find out about the supported resolutions of your camera model.",
                       default = "1920x1080")

args = parser.parse_args()
dirname = args.imgdir

# Check if resolution is specified correctly
if not "x" in args.res:
    print("Specify resolution with x as WxH. (Example: 1920x1080).")
    exit()
imgW, imgH = map(int, args.res.split("x"))


# Create a folder, if it doesn't exist
cwd = getcwd()
dirpath = path.join(cwd,dirname)
if not path.exists(dirpath):
    makedirs(dirpath)

# Prevent taken frame overwriting
imgnum  = 15949
key_flag = 0

#img_exists = 1
# while img_exists: # Image exists
#     #imgname = dirname + "_" + str(imgnum) + ".png"
#     imgname = "".join([dirname, "_", str(imgnum), ".png"])# faster
#     imgpath = path.join(dirpath,imgname)
#     if path.exists(imgpath): # proof if image number is already taken
#         imgnum += 1
#     else:
#         img_exists = 0 # Image doesn't exists
while 1:
    filename = f"{dirname}_{imgnum}.png"
    if not path.exists(path.join(dirpath, filename)):
        break
    imgnum +=1

#### Initialize camera #####
# Load the tuning for the RPi IR-Cut camera.
# Renamed the original file (ov5647.json) to custom.
tuning_file = Picamera2.load_tuning_file("ov5647_custom.json")
# Call picamera2 constructor and pass loaded tuning file.
picam2 = Picamera2(tuning=tuning_file)
# Set options for saving images
picam2.options["quality"] = 95 # best quality
picam2.options["compress_level"] = 0 # no compression
# Apply preview configuration for the camera. Change format to XRGB8888 (RGB), default XBGR8888 (RGBA)

# Create preview configuration without denoising
#picam2.configure(picam2.create_preview_configuration(main={"format": "XRGB8888", "size": (imgW, imgH)}))

# Create preview configuration with denoising
picam2.configure(picam2.create_preview_configuration(main={"format": "XRGB8888", "size": (imgW, imgH)},
                                                     controls={"NoiseReductionMode":controls.draft.NoiseReductionModeEnum.HighQuality}))

# Print the hints for the user
print("\n###################")
print("### Image taker ###")
print("###################")
print("For help run the script with the '--help' option.")
print("\nPress 'p' to take an image, they will be saved in the '{}' folder.".format(dirname))
print("To quit the application press 'q'.\n")

# Create preview window
picam2.start_preview(Preview.QTGL, x=915, y=72, width=1000, height=900) # QTGL most effiecient way of displaying
picam2.start()

try:
    while 1:
        if is_pressed("p"):
            if key_flag == 0:
                key_flag = 1
                filename = "".join([dirname, "_", str(imgnum), ".png"])
                savepath = path.join(dirpath, filename)
                # old without request
                #picam2.capture_file(savepath,  "main", format="png", wait=None)
                
                # new with capture request
                request = picam2.capture_request()
                request.save("main", savepath, format="png")
                print("\rPicture taken and saved as -> {}.".format(filename))
                request.release()
                imgnum += 1 
            else:
                key_flag = 0
        if is_pressed("q"):
            print("\r++++++++++++++++++++++++++++++++++++++++++++++")
            print("\rInterruption: stop preview and close camera...")
            break           
finally:
    picam2.stop_preview()
    picam2.stop()
    picam2.close()
    tcflush(stdin, TCIOFLUSH)
