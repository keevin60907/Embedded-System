# FaceID Monitor

## Features
- Face Detection
- Motion Detection
- Mail alarm
- Python module with tunable parameters

## Scenario
The camera keeps detecting motion. When motion is detected, the authorized face must be detected within a buffer time to release the alarm; otherwise, the buzzer will ring, and Pi will send images by e-mail.

## Requirements
SMTP function must be installed, which is not contained in python functions. Refer to the reference below to setup the SMTP server.
Other modules that are required are:
- click==6.7
- Flask==0.12.2
- itsdangerous==0.24
- Jinja2==2.9.6
- MarkupSafe==1.0
- picamera==1.13
- Werkzeug==0.12.2
- numpy==1.13.1
- opencv-python==4.0.0


## Software Structure
![](https://i.imgur.com/740wdIn.jpg)

![](https://i.imgur.com/tDJzSyo.jpg)

![](https://i.imgur.com/sIGC7Zr.jpg)

![](https://i.imgur.com/3QsjvMw.jpg)

![](https://i.imgur.com/Uhlpe6y.jpg)

![](https://i.imgur.com/bOzZJe3.jpg)

## How to use

### Face registeration
First, you have to register your face into the machine. By uploading your photos (recommended less than 2K in both width and length) into the `dataset/` directory. You should create a new folder named as your name and put your photos into the folder. e.g.
- `dataset/Mike/IMG_0001.JPG`
- `dataset/Mike/IMG_0002.JPG`
- `dataset/Mike/IMG_0003.JPG`
- `dataset/Kevin/IMG_0045.JPG`
- `dataset/Kevin/IMG_0049.JPG`
- `dataset/Kevin/IMG_0148.JPG`

After that, execute `python3 encode_faces.py` to encode faces into a single file. Then this file will be used by the following face detection module

### Setup your mail address and message
In `mail.txt`, you can set your own mail. Note that `FROM/TO/Subject` rows must be included; otherwise the mail may fail to be sent out.

### Merging all the functions
Last, execute `python3 app.py` to run all the functions including **http streaming**, **motion detection**, **face detection**, **LED and buzzer alarm**, and **mail alarm**

## Tunable parameters
- In `camera_opencv.py`,
    - `ALARM_BUFFER`: buffer time after motion is detected. This value can be set larger if false alarm is too frequent
    - `AUTH_BUFFER`: buffer time after face detection to prevent frequent face detection which may sometimes be annoying. Set this value lower if miss happens.
    - `ALARM_DURATION`: max time that alarm will last.

- In `mail.txt`,
    - `FROM:` the sender name that will be presented by the mail receiver
    - `TO:` the receiver mail address
    - `BCC:` BCC address if needed
    - `Reply-To:` the reply-to address for this mail
    - `Subject:` the subject of this mail

- In `dataset/`, create your own folders with your name as folder name, containing photos of yours

## References
- https://github.com/miguelgrinberg/flask-video-streaming 
- https://www.hackster.io/gulyasal/make-a-mail-server-out-of-your-rpi3-5829f0 
- https://www.pyimagesearch.com/2018/06/25/raspberry-pi-face-recognition/ 
- https://blog.gtwang.org/programming/opencv-motion-detection-and-tracking-tutorial/
