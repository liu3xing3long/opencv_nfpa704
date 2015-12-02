# Targets are listed alphabetically. Refer to target "all" for execution order.
# Warning: If executing targets in a Vagrant VM, the VM date and time may not be
# congruent with those of the host system. This will lead to Make warnings at
# best or unnecessary target re-execution at worst.
# Warning: this Makefile is designed to be run from its directory, not outside.

# Note: Make uses "lazy set." Variables are recursively explanded when used.
# A new variable is created when its value is used across two or more targets.
IMGDIR_BASE=images
IMGDIR_NEG=$(IMGDIR_BASE)/negative
IMGDIR_POS=$(IMGDIR_BASE)/positive
NEGLIST_PATH=$(TMPDIR)/negatives.txt
SMPLDIR=$(TMPDIR)/samples
SRCDIR=src
TMPDIR=training
VEC_PATH=$(TMPDIR)/cropped.vec

.PHONY: all clean negatives positives samples vec

# This target will execute the training from start to finish. It will take a
# very long time.
all: negatives positives samples vec

# Warning: this step takes a very, very long time.
cascade: | $(NEGLIST_PATH) $(VEC_PATH)
	mkdir -p $(TMPDIR)/cascade
	opencv_traincascade \
		-data $(TMPDIR)/cascade \
		-vec $(VEC_PATH) \
		-bg $(NEGLIST_PATH) \
		-featureType HAAR \
		-numPos 4550 -numNeg 601 \
		-numStages 20 precalcValBufSize 1024 -precalcIdxBufSize 1024 \
		-w 48 -h 48

# Warning: this removes all generated files including positive sample images.
clean: | $(TMPDIR)
	rm -R $(TMPDIR)
	rm -R $(IMGDIR_POS)

# Regex will match both PNG and JPG. File listing order will be arbitrary.
# Probably better for random selection by opencv_createsamples anyway.
# Note the sed invokation to prepend a relative prefix to the paths.
negatives: | $(IMGDIR_NEG)
	mkdir -p $(TMPDIR)
	find $(IMGDIR_NEG) -regextype posix-extended -regex '.*\.(png|jpg)' \
		| sed 's/^/..\//' \
		> $(NEGLIST_PATH)

positives: | $(SRCDIR)/assemble_positives.py $(SRCDIR)/positive_components
	mkdir -p $(IMGDIR_POS)
	python $(SRCDIR)/assemble_positives.py $(SRCDIR)/positive_components \
		$(IMGDIR_POS)

# Warning: this step takes a long time.
samples: | $(SRCDIR)/create_samples.py $(IMGDIR_POS) $(NEGLIST_PATH)
	mkdir -p $(SMPLDIR)
	python $| $(SMPLDIR)

# Warning: The values hard-coded into the arguments here are based on the
# arguments passed to opencv_createsamples in the "samples" target. The time
# required to dynamically calculate the necessary values outweighs the returns
# for such a limited use case and audience.
vec: | $(SMPLDIR)
	cat $(SMPLDIR)/*.png.txt > $(SMPLDIR)/positives.txt
	opencv_createsamples \
		-info $(SMPLDIR)/positives.txt \
		-bg $(NEGLIST_PATH) \
		-vec $(VEC_PATH) \
		-num 5000 -w 48 -h 48



