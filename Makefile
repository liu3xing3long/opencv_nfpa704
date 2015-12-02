# Warning: If executing targets in a Vagrant VM, the VM date and time may not be
# congruent with those of the host system. This will lead to Make warnings at
# best or unnecessary target re-execution at worst.

IMGDIR_BASE=images
IMGDIR_POS=$(IMGDIR_BASE)/positive
SRCDIR=src

.PHONY: positives

positives: | $(SRCDIR)/assemble_positives.py $(SRCDIR)/positive_components
	mkdir -p $(IMGDIR_POS)
	python $(SRCDIR)/assemble_positives.py $(SRCDIR)/positive_components $(IMGDIR_POS)
