#!/bin/bash

today=$(date +"%Y%m%d")
dir="Atmos_Timelapse_${today}"
path="${dir}/${today}.mp4"
if [ -d ${dir} ]; then
  ffmpeg -framerate 30 \
         -pattern_type glob \
         -i "${dir}/*.jpg" \
         -s:v 1440x1080 \
         -c:v libx264 \
         -crf 17 \
         -pix_fmt yuv420p \
         ${path}
fi

s3cmd put -P ${path} s3://atmos-timelapse/${today}.mp4
