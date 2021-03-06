#!/bin/python

import picamera
import argparse
from datetime import datetime, date
import socket
import time
import os

def get_default_filename():
    now = datetime.now()
    date_str = now.strftime("%Y%m%d")
    time_str = now.strftime("%H%M%S")
    return "_".join(["Atmos", date_str, time_str])

def get_default_video_filename():
    return get_default_filename() + ".h264"

def get_defailt_image_filename():
    return get_default_filename() + ".jpg"

def record_to_file(camera, filename, duration):
    stream = open(filename, "wb")
    record(camera, stream, duration)
    stream.close()

def record_to_sock(camera, port, duration):
    sock = socket.socket()
    sock.bind(("0.0.0.0", port))
    sock.listen(0)
    connection = sock.accept()[0].makefile('wb')
    record(camera, connection, duration)

def record(camera, stream, duration):
    camera.start_preview()
    camera.start_recording(stream, format='h264', quality=23)
    camera.wait_recording(duration)
    camera.stop_recording()

def timelapse(camera, period):
    today = date.today()
    dir_name = '_'.join(['Atmos', 'Timelapse', today.strftime('%Y%m%d')])
    if not os.path.isdir(dir_name):
      os.mkdir(dir_name)
    os.chdir(dir_name)

    camera.start_preview()
    for filename in camera.capture_continuous('{timestamp:%H%M}.jpg'):
        time.sleep(period)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", default="record-to-file")
    parser.add_argument("-o", "--output", default=get_default_video_filename())
    parser.add_argument("-d", "--duration", default=10, type=int)
    parser.add_argument("-p", "--port", default=8000, type=int)
    args = parser.parse_args()

    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.awb_mode = 'auto'

    if args.action == "record-to-file":
        record_to_file(camera, args.output, args.duration)
    elif args.action == "record-to-socket":
        record_to_sock(camera, args.port, args.duration)
    elif args.action == "timelapse":
        timelapse(camera, 60)

if __name__ == '__main__':
    main()

