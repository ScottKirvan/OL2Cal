#!/usr/bin/env python3

# processes one liner pdf into a google calendar csv file
# %%
#from __future__ import print_function
import re
import pdfplumber
import datetime
#import argparse
import os
import math
#
import ProcessCL

# %%
args = ProcessCL.Init()

# %%
import sys
import contextlib

@contextlib.contextmanager
def smart_open(filename=None):
    if filename and filename != '-':
        fh = open(filename, 'w')
    else:
        fh = sys.stdout

    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()

# writes to some_file
#with smart_open(args.outfile) as fh:
#    print('some output 1', file=fh)

# writes to stdout
#with smart_open() as fh:
#    print('some output 2', file=fh)

# writes to stdout
#with smart_open('-') as fh:
#    print('some output 3', file=fh)

#exit()

# %%
# grab the pdf as text

oneliner = args.infile[0]


import inspect
frame = inspect.currentframe()

from DBPrint import DebugPrint 
import DBPrint
#DebugPrint(__file__, frame.f_lineno, "boowah!  %s, and %d, and %d" % (oneliner, 2, 3))
DBPrint.SetEnabled(args.debug)

text=''
with pdfplumber.open(oneliner) as pdf:
    for page in pdf.pages:
        text += page.extract_text() + '\n'

# %%
# break that text into an array of lines
line = []
for line_tmp in text.split('\n'):
    line.append(line_tmp)
    
if (args.dumppdf):
    for f in line:
        print (f)
    exit()

# %%
from dataclasses import dataclass
@dataclass
class events:
    days = []
    day_num = []
    set_loc = []
    call = []
    wrap = []

if (args.format == 'FAM1'):
    days_re = re.compile(r'\* Day') # todo - need a better regex - specify start of line
    ampm_re = re.compile(r'pm \*') # todo - need a better regex - specify end of line 
    endday_re = re.compile(r'End Day # ') # todo - need a better regex - specify start of line
elif (args.format == 'FAM2'):
    import FAM2
    FAM2.Process(events, line)
else:
    print ("Error: Unknown format, \"%s\"" % (args.format))
    exit()

# %%
# format and output the data
# todo - put in code to escape all commas in strings
with smart_open(args.outfile) as fh:
    Subject = "Subject"
    Start_Date = "Start Date"
    Start_Time = "Start Time"
    End_Date = "End Date"
    End_Time = "End Time"
    All_day_event = "All day event"
    Description = "Description"
    Location = "Location"
    Private = "Private"
    Commas = ",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,"

    row = ""
    row += Subject + ","
    row += Start_Date + ","
    row += Start_Time + ","
    row += End_Date + ","
    row += End_Time + ","
    row += All_day_event + ","
    row += Description + ","
    row += Location + ","
    row += Private + ","
    row += Commas
    print (row, file=fh)

    i = 0
    DebugPrint(__file__, frame.f_lineno, "len(events.days):  %s" % (len(events.days)))
    while i < len(events.days):
        Subject = "Day " + str(events.day_num[i]) + " - " + str(events.set_loc[i])
        Start_Date = str(events.call[i].strftime("%m/%d/%Y"))
        Start_Time = (events.call[i].strftime("%I:%M %p"))
        All_day_event = "FALSE"
        End_Date = str(events.wrap[i].strftime("%m/%d/%Y"))
        End_Time = (events.wrap[i].strftime("%I:%M %p"))
        Location = str(events.set_loc[i])
        Private = "FALSE"
        Description = "Origin file: " + os.path.basename(args.infile[0])

        row = ""
        row += Subject + ","
        row += Start_Date + ","
        row += Start_Time + ","
        row += End_Date + ","
        row += End_Time + ","
        row += All_day_event + ","
        row += Description + ","
        row += Location + ","
        row += Private + ","
        row += Commas
        print (row, file=fh)
        i += 1

# eof