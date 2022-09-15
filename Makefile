all : test

.PHONY: test
test:
	python3 src/OL2Cal.py private/FAM1.pdf
