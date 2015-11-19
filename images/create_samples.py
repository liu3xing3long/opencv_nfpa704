import glob
import os
import subprocess
import time

# Enumerate positive images.
imagePositiveGlob = os.path.join(
  'positive',
  '*.png'
)
imagePositivePaths = glob.glob(imagePositiveGlob)

for imagePath in imagePositivePaths:
  subprocess.call(
    'opencv_createsamples'
    + ' -img ' + imagePath
    + ' -bg negatives.txt'
    + ' -info training/' + os.path.basename(imagePath) + '.txt'
    + ' -num 20 -w 300 -h 300 -bgthresh 0 -bgcolor 40',
    shell=True
  )
  time.sleep(5)

