######## PiCamera2 picture taker for the RPI IR-Cut camera #########

# Author: Petros626
# forked from/oriented on: https://github.com/EdjeElectronics/Image-Dataset-Tools/blob/main/PictureTaker/PictureTaker.py
# Date: 28.02.2023
# Description: 
# This program takes pictures (.png format - 95% quality and 0 compression) from the RPi IR-Cut
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


# Define ImageTaker class to handle capturing images from camera
class ImageTaker:
    # Class attributes
    # Load the tuning for the RPi IR-Cut camera. Added 'rpi.sharp' parameter to custom.
    tuning_file = Picamera2.load_tuning_file("ov5647_custom.json")
    # Call picamera2 constructor and pass loaded tuning file. Set options for saving images
    picam2 = Picamera2(tuning=tuning_file)
    picam2.options["quality"] = 95 # best quality
    picam2.options["compress_level"] = 0 # no compression
   
    # Constructor with instance attributes
    def __init__(self, imgdir, res):
        self.imgdir = imgdir
        self.res = res
        self.imgnum = 1
        self.key_flag = 0
        self.dirpath = None
        self.preview_config = None
        self.initialize_camera()
        
    # Function to check passed resolution and initiliaze the camera with parameters
    def initialize_camera(self):
        # Check if resolution is specified correctly
        if not "x" in self.res:
            print("Specify resolution with x as WxH. (Example: 1920x1080).")
            exit()
        imgW, imgH = map(int, self.res.split("x"))
        
        # Apply preview configuration for the camera.
        # Change format to XRGB8888 (RGB), default XBGR8888 (RGBA)
        if not self.preview_config:
            # with denoising
            self.preview_config= self.picam2.create_preview_configuration(main={"format": "XRGB8888", "size": (imgW, imgH)},
                                                                          controls={"NoiseReductionMode": controls.draft.NoiseReductionModeEnum.HighQuality})
            # without denoising
            #self.picam2.configure(self.picam2.create_preview_configuration(main={"format": "XRGB8888", "size": (imgW, imgH)}))
        self.picam2.configure(self.preview_config)
  
    # Function to set and start the preview window    
    def start_preview(self):
        # Create preview window. QTGL most effiecient way of displaying
        self.picam2.start_preview(Preview.QTGL, x=915, y=72, width=1000, height=900)
        self.picam2.start()
        
    # Function for the capturing process    
    def capture_image(self):
        filename = f"{self.imgdir}_{self.imgnum}.png"
        if not path.exists(path.join(self.imgdir, filename)):
            savepath = path.join(self.imgdir, filename)
            request = self.picam2.capture_request()            
            request.save("main", savepath, format="png")
            print("\rPicture taken and saved as -> {}.".format(filename))
            request.release()
        self.imgnum += 1
        
    # Function to stop the preview window  
    def stop_preview(self):
        self.picam2.stop_preview()
        
    # Function to stop and close the camera      
    def close(self):
        self.picam2.stop()
        self.picam2.close()
        
    # Function to check, if image save folder exists   
    def check_folder(self):
        # Create a folder, if it doesn't exist
        # # If the directory path has been cached, no need to check again
        if self.dirpath is None:
            return 
        dirname = self.imgdir
        cwd = getcwd()
        dirpath = path.join(cwd, dirname)
        if not path.exists(dirpath):
            makedirs(dirpath)
            self.dirpath = dirpath
            
   # Function to run the image capturing     
    def run(self):
        # Print the hints for the user
        print("\n###################")
        print("### Image taker ###")
        print("###################")
        print("For help run the script with the '--help' option.")
        print("\nPress 'p' to take an image, they will be saved in the '{}' folder.".format(self.imgdir))
        print("To quit the application press 'q'.\n")
        self.check_folder()
    
        try:
            while 1:
                if is_pressed("p"):
                    if self.key_flag == 0:
                        self.key_flag = 1
                        self.capture_image()
                    else:
                        self.key_flag = 0
                if is_pressed("q"):
                    print("\r++++++++++++++++++++++++++++++++++++++++++++++")
                    print("\rInterruption: stop preview and close camera...")
                    break           
        finally:
            capture_thread.stop()
            self.stop_preview()
            self.close()
            tcflush(stdin, TCIOFLUSH)
    
if __name__ == "__main__":
    # Fetch script arguments
    parser = ArgumentParser()
    parser.add_argument("--imgdir",
                        help = "Folder where the taken images get saved. If you not specify there will be created one automatically.",
                        default = "images")
    parser.add_argument("--res",
                        help = "Required resolution in WxH. To avoid erros find out about the supported resolutions of your camera model.",
                       default = "1920x1080")
    args = parser.parse_args()
    
    # Create an object image_taker of the class
    image_taker = ImageTaker(args.imgdir, args.res)
    image_taker.start_preview()
    image_taker.run()