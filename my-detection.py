import Jetson.GPIO as GPIO
import jetson_inference
import jetson_utils
import argparse
import sys
import json
import time

datas_path = "datas.json"
# Initialize variables for fruit counts
banana = 0
orange = 0
apple = 0
strawberry = 0
pear = 0


# Pin numbers
pin0 = 12 # input
pin1 = 16 # output 
pin2 = 18 # output

# Set GPIO pin mode
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin0, GPIO.IN)
GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)

# parse the command line
parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, default="/dev/video0", nargs='?', help="URI of the input stream")
#parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="model to use, can be:  googlenet, resnet-18, ect.")
parser.add_argument("--topK", type=int, default=3, help="show the topK number of class predictions")
parser.add_argument("--threshold", type=float, default=0.4, help="minimum detection threshold to use")
parser.add_argument("--overlay", type=str, default="labels", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'") 
args = parser.parse_args()

#net = jetson_inference.detectNet(args.network, sys.argv, args.threshold)
net = jetson_inference.detectNet(model="./jetson-inference/python/training/detection/ssd/models/ssd-mobilenet-fruit/ssd-mobilenet.onnx", labels="/jetson-inference/python/training/detection/ssd/models/ssd-mobilenet-fruit/labels.txt ",input_blob="input_0", output_cvg="scores", output_bbox="boxes",threshold=args.threshold)

input = jetson_utils.videoSource(args.input,  options={'width': 1920, 'height': 1080})

font = jetson_utils.cudaFont()
tahmin = 0
while True:
    data = {}
    
    try:

       GPIO.output(pin1, GPIO.HIGH)
       GPIO.output(pin2, GPIO.LOW)

    except KeyboardInterrupt:
       GPIO.cleanup()
    while GPIO.input(pin0):
       GPIO.output(pin1, GPIO.LOW)
       GPIO.output(pin2, GPIO.LOW)

       # capture the next image
       img = input.Capture()
       if img is None: # timeout
            continue
         
       time.sleep(6)

       detections = net.Detect(img, overlay=args.overlay)

       print("detected {:d} objects in image".format(len(detections)))

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

    # Update Changes
       data['banana'] = banana
       data['apple'] = apple
       data['orange'] = orange
       data['pear'] = pear
       data['strawberry'] = strawberry

    # Write the datas to json file
       with open("datas.json", "w") as file:
           json.dump(data, file, indent=6)

       print("JSON ok")
    
       
       # Set to Pin start position
       GPIO.output(pin1, GPIO.HIGH)
       GPIO.output(pin2, GPIO.LOW)

       # Yorum gelecek
       time.sleep(3)
       
       # exit on input/output EOS
       if not input.IsStreaming():
           break
