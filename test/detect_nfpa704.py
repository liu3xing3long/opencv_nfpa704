# A very simple script to test the cascade. Passed a path to a JPG or PNG image,
# this will run the cascade against the image and display a temporary image
# with the detections outlined in blue rectangles. The image will display for
# ten seconds or until any key is pressed.
# @param testImagePath {string} The path to the image on which detection should
#   should be run.

import cv2 as cv
import os
import sys

testImagePath = os.path.realpath(sys.argv[1])

cascade = cv.CascadeClassifier('../images/cascade/48x5000/cascade.xml')
image = cv.imread(testImagePath)
greyscaleImage = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
objects = cascade.detectMultiScale(greyscaleImage)

for (coordX, coordY, width, height) in objects:
    cv.rectangle(
      image,
      (coordX, coordY),
      (coordX + width, coordY + height),
      (255, 0, 0),
      2
    )
cv.imshow('result', image)
cv.waitKey(10000)
cv.destroyAllWindows()

