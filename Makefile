IN_FILE := private/FAM2.pdf
IN_FMT := FAM2
OUT_FILE := out/test.csv

# If the first argument is "run"...
# valid run args are currently "FAM1" or "FAM2"
ifeq (run,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

.PHONY: run
run: 
	@echo prog $(RUN_ARGS)
	src/OL2Cal.py --format $(RUN_ARGS) -o $(OUT_FILE) private/$(RUN_ARGS).pdf

all : stdout

.PHONY: stdout
stdout:
	src/OL2Cal.py --format $(IN_FMT) $(IN_FILE)

.PHONY: fileout
fileout:
	src/OL2Cal.py --format $(IN_FMT) -o $(OUT_FILE) $(IN_FILE)

.PHONY: noargs
noargs:
	src/OL2Cal.py 

.PHONY: help
help:
	src/OL2Cal.py -h

.PHONY: dump
dump:
	src/OL2Cal.py -d $(IN_FILE)

.PHONY: outdir
outdir:
	mkdir -p out
	src/OL2Cal.py -o $(OUT_FILE) $(IN_FILE):w


