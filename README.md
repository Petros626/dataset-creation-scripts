## Python scripts for creating the dataset

Manually take and save pictures:
```python
ir_cut_picamera2.py: 
```

Same as above as OOP approach (just for learning purposes):
```python
ir_cut_picamera2_oop.py:
```

The first script is used to manually take and save pictures. The second is a copy of the first but with an object-oriented approach. 


## Use of the Scripts
Both scripts need the folder, where the taken images should be saved. If no folder is created before and passed as argument, the script will automatically create a default folder called "images". The default resolution is 1920x1080, if you want to change it don't forget to specify WxH with x.

**Note**: The 'sudo' command is required for permissions of the package [keyboard](https://github.com/boppreh/keyboard)

```python 
sudo python3 ir_cut_picamera2.py --imgdir=images --res=1920x1080
```

```python
sudo python3 ir_cut_picamera2_oop.py --imgdir=images --res=1920x1080
```

The last script needs the destination, where the calibration images for [OpenCV](https://github.com/opencv/opencv) [Camera Calibration](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html) get saved. Additionally you can adjust the time before a picture is taken, to position the chessboard before taking the image. To achieve a sufficient accuracy it's recommended to take between 10-20 images of the chessboard.
