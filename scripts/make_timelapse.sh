#!/bin/bash

today=$(date +"%Y%m%d")
path="Atmos_Timelapse_${today}"
if [ -d ${path} ]; then
  ffmpeg -framerate 30 \
         -pattern_type glob \
         -i "${path}/*.jpg" \
         -s:v 1440x1080 \
         -c:v libx264 \
         -crf 17 \
         -pix_fmt yuv420p \
         ${path}/${today}.mp4
fi

