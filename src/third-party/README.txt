This directory contains scripts and utilities provided by third parties and used
in this project either directly or as a reference. The objects, sources, and any
additional information are provided below.

createtrainsamples.pl
  http://note.sonots.com/SciSoftware/haartraining.html#o40a43fd
  http://note.sonots.com/SciSoftware/haartraining.html#v6f077ba
mergevec.cpp
  http://note.sonots.com/SciSoftware/haartraining.html#o40a43fd
  http://note.sonots.com/SciSoftware/haartraining/mergevec.cpp.html
  Compilation:
    Find haartraining/ directory in OpenCV source code directory tree.
    Copy mergevec.cpp to haartraining/ directory. If you are working on linux,
    g++ `pkg-config --cflags opencv` `pkg-config --libs opencv` -o mergevec
    mergevec.cpp cvboost.cpp cvcommon.cpp cvsamples.cpp cvhaarclassifier.cpp
    cvhaartraining.cpp


