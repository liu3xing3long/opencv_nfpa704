# This script automates the generation of multiple positive samples from each
# positive image in the specified positive image directory.
#
# The opencv_createsamples utility, when called with the arguments seen below,
# opens each positive image, applies random persective transforms, and places
# the result on a random negative image found in the negative image directory.
# The resulting composite images, along with a .txt (info) file containing the
# the coordinates of the positive image within the negative, are saved to the
# output directory.
#
# The time delay is an unfortunate necessity when interacting with
# opencv_createsamples in this way. When executed on images too quickly in
# succession, there quickly arise inconsistencies between the composite images
# generated and the data recorded in the info files. I suspect this is a
# filesystem race condition issue but given my experience with OpenCV thus far,
# I am certainly not ruling out a bug in the createsamples utility.
#
# Don't change the opencv_createsamples arguments unless you know what you're
# doing.
#
# @param positivesDirPath {string} The path to the positive images.
# @param negativesFilePath {string} The path to the file in which negative images
#   are enumerated.
# @param outputDirPath {string} The path of the directory into which the
#   composite images and info files should be saved.

import glob
import os
import subprocess
import sys
import time

# Still neither validation nor sanitization.
positivesDirPath = os.path.realpath(sys.argv[1])
negativesFilePath = os.path.realpath(sys.argv[2])
outputDirPath = os.path.realpath(sys.argv[3])

# Enumerate positive images.
positiveImgGlob = os.path.join(
  positivesDirPath,
  '*.png'
)
positiveImgPaths = glob.glob(positiveImgGlob)

for positiveImgPath in positiveImgPaths:
  infoFilePath = os.path.join(
    outputDirPath,
    os.path.basename(positiveImgPath) + '.txt'
  )
  subprocess.call(
    'opencv_createsamples'
    + ' -img ' + positiveImgPath
    + ' -bg ' + negativesFilePath
    + ' -info ' + infoFilePath
    + ' -num 4 -w 48 -h 48 -bgthresh 0 -bgcolor 40',
    shell = True
  )
  time.sleep(5)
