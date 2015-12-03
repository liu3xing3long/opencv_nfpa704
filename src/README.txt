DIRECTORIES
positive_components:
  A directory of individual images ready for composition into complete NFPA 704
  symbols.
  Current dimensions:
    diamonds = 300 x 300
    quadrant contents (digits and special) = 71 x 71
work_files: A directory in which the "source" Inkscape SVG files are
  stored. These SVGs were used to create, size, and export the files found in
  the positive_components directory.

ADDITIONAL NOTES
Ideally, training would account for:
  font typefaces
  character weights
  character sizes
  "water reactive" symbol strikethrough placement relative to "W" character
  lateral coplacement of "water reactive" and "oxidizer" special symbols instead
    of vertical
To improve classifier performance:
  increase transform angles of positive sample generation
  Greatly expand and increase variety of negative image pool
  increase positive sample dimensions
