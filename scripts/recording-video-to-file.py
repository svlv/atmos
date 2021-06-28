#!/bin/python

import picamera
import argparse
from datetime import datetime

def det_default_filename():
    now = datetime.now()
    date_str = now.strftime("%Y%m%d")
    time_str = now.strftime("%H%M%S")
    return "_".join(["Atmos", date_str, time_str])

def get_default_video_filename():
    return det_default_filename() + ".h264"

def record_to_file(filename, duration):
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    stream = open(filename, "wb")
    camera.start_recording(stream, format='h264', quality=23)
    camera.wait_recording(duration)
    camera.stop_recording()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", dest="output", default=get_default_video_filename())
    parser.add_argument("-d", dest="duration", default=10, type=int)
    args = parser.parse_args()
    
    record_to_file(args.output, args.duration)

if __name__ == '__main__':
    main()
