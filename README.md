## Python scripts for creating several images or a dataset

This repository contains scripts to create images or a data set with a compatible camera for the Raspberry Pi. The API used is [PiCamera2](https://github.com/raspberrypi/picamera2).

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


