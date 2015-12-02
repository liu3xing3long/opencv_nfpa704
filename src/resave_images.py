# This file, when executed and supplied a path to a target directory, will open
# each JPG and PNG image and resave each in PNG format under a new name. As most
# training and test images were pulled from random hosts on the Internet, the
# operations performed by this script normalize file names and in theory
# sanitize the image files of any attempt at malicious code inclusion,
# correcting color profile errors in the process. PNG format is uniformally used
# to avoid the degredation of image quality over repeated JPG compression on an
# image. The original image files are deleted after the resave operations.
#
# Ideally, this would copy target directory's contents to temp directory on
# on which operations will be performed. This would enable a transaction-like
# series of changes rather than destructive modification to original files that
# is irreversible in the case of fatal errors.
#
# @param directoryPath {string} The directory in which the image files exist.
# @warning The original image files are deleted.

import os
from PIL import Image
import sys

directoryPath = os.path.realpath(sys.argv[1])

iterationCount = 0
for srcFileName in os.listdir(directoryPath):
  srcFilePath = os.path.join(directoryPath, srcFileName)
  srcFileNameSplit = srcFileName.split('.')
  srcFileExtension = srcFileNameSplit[len(srcFileNameSplit) - 1]
  if srcFileExtension == 'jpg' or srcFileExtension == 'png':
    destFileName = str(iterationCount).zfill(3) + '.png'
    image = Image.open(srcFilePath)
    image = image.convert('RGB')
    image.save(os.path.join(directoryPath, destFileName))
    os.remove(srcFilePath)
    iterationCount += 1
  else:
    print('failed: ' + srcFilePath)

