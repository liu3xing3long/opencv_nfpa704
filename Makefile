# Warning: If executing targets in a Vagrant VM, the VM date and time may not be
# congruent with those of the host system. This will lead to Make warnings at
# best or unnecessary target re-execution at worst.

IMGDIR_BASE=images
IMGDIR_NEG=$(IMGDIR_BASE)/negative
IMGDIR_POS=$(IMGDIR_BASE)/positive
SRCDIR=src
TMPDIR=training

.PHONY: all clean negatives positives

all: negatives positives

# Warning: this removes all generated files including positive sample images.
clean: | $(TMPDIR)
	rm -R $(TMPDIR)
	rm -R $(IMGDIR_POS)

# Regex will match both PNG and JPG. File listing order will be arbitrary.
# Probably better for random selection by opencv_createsamples anyway.
negatives: | $(IMGDIR_NEG)
	mkdir -p $(TMPDIR)
	find $(IMGDIR_NEG) -regextype posix-extended -regex '.*\.(png|jpg)' > $(TMPDIR)/negatives.txt

positives: | $(SRCDIR)/assemble_positives.py $(SRCDIR)/positive_components
	mkdir -p $(IMGDIR_POS)
	python $(SRCDIR)/assemble_positives.py $(SRCDIR)/positive_components $(IMGDIR_POS)
