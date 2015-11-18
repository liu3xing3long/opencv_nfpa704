DIRECTORIES
positive_components:
  A directory of individual images ready for composition into complete NFPA 704
  symbols.
  Current dimensions:
    diamonds = 300 x 300
    quadrant contents (digits and special) = 70 x 70
work_files: A directory in which the "source" Inkscape SVG files are
  stored. These SVGs were used to create, size, and export the files found in
  the positive_components directory.

COMMANDS
Assemble positive images:
  cd {projectRoot}/src
  python assemble_positives.py positive_components ../images/positive

Create negatives.txt:
  cd {projectRoot}/images/positives
  find ../negative -regextype posix-extended -regex '.*\.(png|jpg)' > negatives.txt

Generate samples and description files:
  Note: For some reason, the program will not always generate the designated
    number of samples. Bumped "-num" samples to 20 to average desired number.
    Ex: for 1250 positives, generated 7915 samples
  cd {projectRoot}/images/positives
  find ./ -name '*.png' -exec opencv_createsamples -img '{}' -bg negatives.txt -info ../training/'{}'.txt -num 20 -w 300 -h 300 -bgthresh 0 -bgcolor 40 \;


ADDITIONAL NOTES
Ideally, training would include variations for:
  font typeface
  character weight
  character size
  "water reactive" symbol strikethrough placement
  lateral coplacement of "water reactive" and "oxidizer" special symbols instead of vertical
