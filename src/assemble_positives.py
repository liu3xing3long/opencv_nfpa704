# This script "assembles" the NFPA 704 symbol components into a series
# of complete and valid NFPA 704 symbols. This script was needed due to the
# high cardinality of valid NFPA 704 symbols given the sheer number of possible
# combinations of components. Every NFPA-standardized digit is included in the
# component set. All permutations of the availabe components are created. This
# script was not designed to be robust or maintainable and is currently suitable
# only for development and testing purposes.
#
# @param componentsDir <string> The absolute or relative filesystem path to the
#   components directory.
# @param outputDir <string> The absolute or relative filesystem path to the
#   directory to which all generated NFPA 704 symbols should be saved.

import glob
import os
from PIL import Image
import sys

# Collect arguments. Not yet any validation or sanitization here.
componentsDirPath = os.path.realpath(sys.argv[1])
outputDirPath = os.path.realpath(sys.argv[2])

# Enumerate blank diamond "templates."
imageComponentsDiamondsGlob = os.path.join(
  componentsDirPath,
  'diamond_*.png'
)
imageComponentsDiamondPaths = glob.glob(imageComponentsDiamondsGlob)

# Enumerate numeric digits for red, yellow, and blue quadrants.
imageComponentsDigitsGlob = os.path.join(
  componentsDirPath,
  'digit_*.png'
)
imageComponentsDigitPaths = glob.glob(imageComponentsDigitsGlob)
imageComponentsDigitPaths.sort()

# Enumerate special (white) quadrant content.
imageComponentsSpecialGlob = os.path.join(
  componentsDirPath,
  'special_*.png'
)
imageComponentsSpecialPaths = glob.glob(imageComponentsSpecialGlob)

quadrantRedCoords = (114, 41)
quadrantBlueCoords = (41, 114)
quadrantYellowCoords = (188, 114)
quadrantWhiteCoords = (114, 188)

# This is going to get ugly. REVISE THIS.
# Don't reopen files constantly. Abstract this.
# Break nested loops into functions? Use itertools.combinations?
# Iterate base diamonds.
imageCount = 0
for baseDiamond in imageComponentsDiamondPaths:
  baseDiamond = Image.open(baseDiamond)

  # Iterate blue digits.
  for digitBluePath in imageComponentsDigitPaths:
    baseDiamondCopyBlue = baseDiamond.copy()
    digitBlueImage = Image.open(digitBluePath)
    baseDiamondCopyBlue.paste(digitBlueImage, quadrantBlueCoords, digitBlueImage)

    # Iterate red digits.
    for digitRedPath in imageComponentsDigitPaths:
      baseDiamondCopyRed = baseDiamondCopyBlue.copy()
      digitRedImage = Image.open(digitRedPath)
      baseDiamondCopyRed.paste(digitRedImage, quadrantRedCoords, digitRedImage)

      # Iterate yellow digits.
      for digitYellowPath in imageComponentsDigitPaths:
        baseDiamondCopyYellow = baseDiamondCopyRed.copy()
        digitYellowImage = Image.open(digitYellowPath)
        baseDiamondCopyYellow.paste(
          digitYellowImage,
          quadrantYellowCoords,
          digitYellowImage
        )

        # Iterate white symbols and save image.
        for digitWhitePath in imageComponentsSpecialPaths:
          baseDiamondCopyWhite = baseDiamondCopyYellow.copy()
          digitWhiteImage = Image.open(digitWhitePath)
          baseDiamondCopyWhite.paste(
            digitWhiteImage,
            quadrantWhiteCoords,
            digitWhiteImage
          )
          baseDiamondCopyWhite.save(
            os.path.join(outputDirPath, str(imageCount) + '.png')
          )
          imageCount += 1


