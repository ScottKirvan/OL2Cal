IN_FILE := private/FAM3.pdf
IN_FMT := FAM3
OUT_FILE := out/test.csv

all : stdout

.PHONY: test
stdout:
	src/OL2Cal.py --format $(IN_FMT) $(IN_FILE)

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
	src/OL2Cal.py -o $(OUT_FILE) $(IN_FILE)

