# My Detection Code
This page contains explanations of the codes that I used in my project. </br>
Before explaining my code, I must mention that I benefited from the jetson-inference GitHub repository for my codes. It's advisable to install the Jetson-inference repository into your project directory. Otherwise, you may encounter errors in some functions within my code due to missing dependencies.
</br> You can download the Jetson-inference library to your local machine from [here](https://github.com/dusty-nv/jetson-inference/blob/master/docs/building-repo-2.md).
</br>You can access the entire code from [here](/my-detection.py).



## Importing Modules
```python
import Jetson.GPIO as GPIO
```
If you import this module within the jetson-inference docker container, you will encounter permission issues with GPIO pins when running your project. Therefore, it will be easier to download the jetson-inference repository to your local machine and install the libraries.

```python
import jetson_inference
import jetson_utils
import argparse
```
When you have properly installed the Jetson-inference repository, the libraries mentioned here will be imported automatically. If you prefer not to install the repository, you can manually import the libraries yourself.

```python
import sys
```
If you are going to use a pre-trained model from within jetson-inference or if you're going to use a model supported by the jetson-inference repository, you should import this part. If you are going to use your own trained model, you don't need to import this part into your project. We will discuss the details in the later stages of the document.

```python
import json
import time
```
If you are using Python 3.6 and later versions, these libraries are already available.

## Descriptions

```python
banana = 0
orange = 0
apple = 0
strawberry = 0
pear = 0
```
Fruits to be recognized from the camera and written to a JSON file.

```python
pin0 = 12 # input
pin1 = 16 # output 
pin2 = 18 # output
```
The definition of GPIO pins. You can access the pinout diagram of the Jetson Nano 2GB Developer Kit from [here](https://developer.nvidia.com/embedded/learn/jetson-nano-2gb-devkit-user-guide).

## Setting up GPIO pins
```python
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin0, GPIO.IN)
GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)
```
I defined 1 input pin for the infrared sensor and 2 output pins for the motor driver.

## Parse the Command Line
You can modify the default values in this section as you wish, or you can specify the desired values when running the program.
```python
parser = argparse.ArgumentParser()
```
Locate objects in a live camera stream using an object detection DNN.
```python
parser.add_argument("input", type=str, default="/dev/video0", nargs='?', help="URI of the input stream")
```
Here we are specifying the streamer from which we will capture the image. Since I'm using a USB camera, I used ***/dev/video0***. If you are using a CSI camera, you should write ***csi://0***.

```python
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="model to use, can be:  googlenet, resnet-18, ect.")
```
If you are going to use a model defined within jetson-inference as mentioned above, you can add this part to your code by default.
```python
parser.add_argument("--topK", type=int, default=3, help="show the topK number of class predictions")
```
Shows the topK number of class predictions. 

```python
parser.add_argument("--threshold", type=float, default=0.4, help="minimum detection threshold to use")
```
If the desired objects aren't being detected in the video feed or you're getting spurious detections, try decreasing or increasing the detection threshold with the --threshold parameter (the default is 0.4)
## Load the Object Detection Network
```python
#net = jetson_inference.detectNet(args.network, sys.argv, args.threshold)
net = jetson_inference.detectNet(model="./jetson-inference/python/training/detection/ssd/models/ssd-mobilenet-fruit/ssd-mobilenet.onnx", labels="/jetson-inference/python/training/detection/ssd/models/ssd-mobilenet-fruit/labels.txt ",input_blob="input_0", output_cvg="scores", output_bbox="boxes",threshold=args.threshold)
```
If you are using a pre-trained model in this section, you should use the expression with the comment line above. If you are using your own model, you can use it as follows.

## The Working Principle of the Project.


```python
while True:
    data = {}
    
    try:

       GPIO.output(pin1, GPIO.HIGH)
       GPIO.output(pin2, GPIO.LOW)

    except KeyboardInterrupt:
       GPIO.cleanup()
```
At the initial state, we start the motor.

```python
 while GPIO.input(pin0):
       GPIO.output(pin1, GPIO.LOW)
       GPIO.output(pin2, GPIO.LOW)
```
If the infrared sensor detects any object, we enter the second while loop and stop the motor.

```python
img = input.Capture()
if img is None: # timeout
      continue
         
time.sleep(6)

detections = net.Detect(img, overlay=args.overlay)
```
We can think of this part as running the camera and taking a picture after 6 seconds. The waiting time here can be less than 6. Allowing the camera to run for a certain period can assist in focusing the camera.
We detect the image after 6 seconds.
```python
for detection in detections:
           #print(detection.ClassID)
           if detection.ClassID == 1:
               print("apple")
               apple = apple + 1
           elif detection.ClassID == 2:
               print("banana")
               banana = banana + 1
           elif detection.ClassID == 4:
               print("orange")
               orange = orange + 1
           elif detection.ClassID == 5:
               print("pear")
               pear = pear + 1
           elif detection.ClassID == 7:
               print("strawberry")
               strawberry = strawberry + 1
```
We save the number of each fruit detected in variables according to the image.

```python
data['banana'] = banana
data['apple'] = apple
data['orange'] = orange
data['pear'] = pear
data['strawberry'] = strawberry


with open("datas.json", "w") as file:
     son.dump(data, file, indent=6)
```
We convert the 'data' variable defined above using our fruit variables to JSON format and save it to our JSON file.

```python
GPIO.output(pin1, GPIO.HIGH)
GPIO.output(pin2, GPIO.LOW)
time.sleep(3)
```
We start our motor again. The delay here is important; otherwise, the infrared sensor will try to read the same fruits from the camera again without allowing the detected fruits to move.

**You're welcome! :smile:**






























