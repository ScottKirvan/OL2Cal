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
# These are the different regex patterns that are used to find specific lines and details - these may need tweaking based on 
# changes in the oneliner.  I think I'd like to see things like this moved to a config file

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
    print (args.format)
    exit()

    #days_re = re.compile(r'^DAY |^DOUBLE ') # todo - need a better regex - specify start of line
#    days_re = re.compile(r'Estimated ') # todo - need a better regex - specify start of line
#    ampm_re = re.compile(r'pm') # todo - need a better regex - specify end of line 
#    endday_re = re.compile(r'End Day # ') # todo - need a better regex - specify start of line
#    locdesc_re = re.compile(r'Int |Ext |INT') # todo - need a better regex

# dig through and find the "important info" for each shooting day
#i = 0
#days = []
#loc_desc = []
#end_day = []
#DebugPrint(__file__, frame.f_lineno, "len(line): (%d)" % (len(line)))
#while i < len(line):
#    if days_re.search(line[i]):  # find the "Estimated Crew Call" line
#        hr_delta = 0
#        days.append(line[i]) # this has our call time (call)
#        DebugPrint(__file__, frame.f_lineno, "days:  %s" % (line[i]))
#        while i < len(line) and not locdesc_re.search(line[i]):
#            i += 1
#        loc_desc.append(line[i]) # this has our script location (set_loc)
#        DebugPrint(__file__, frame.f_lineno, "loc_desc:  %s" % (line[i]))
#        while i < len(line) and not endday_re.search(line[i]):
#            i += 1
#        end_day.append(line[i]) # this has our day number (day_num) and call date (call_date)
#        DebugPrint(__file__, frame.f_lineno, "end_day: (%d) %s" % (i, line[i]))
#    i += 1
#
## %%
## from that "important info", extract actual details that we want to import to gcal
#i = 0
#call_date = [] # temp var
#day_num = []
#set_loc = []
#calltime_object = [] # includes date - temp var
#call = []
#wrap = []
#DebugPrint(__file__, frame.f_lineno, "%d days" % (len(days)))
#while i < len(days):
#    # extract all the numbers we need to process the Day line (day, call time)
#    array = re.findall(r'[0-9]+', end_day[i]) 
#
#    # parse out day number (day_num)
#    DebugPrint(__file__, frame.f_lineno, "day_num:  %s" % (array[0]))
#    day_num.append(array[0])
#
#    DebugPrint(__file__, frame.f_lineno, "array:  %s" % (array))
#
#    # parse out call date (call_date)
#    matches = re.findall(
#        r'((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d+,\s+\d+)',
#        end_day[i])
#    input_format = "%B %d, %Y" # full month name, day and year
#    output_format = "%m/%d/%Y"
#    for match in matches:
#        new_date = datetime.datetime.strptime(match, input_format).strftime(output_format)
#        call_date = new_date
#    DebugPrint(__file__, frame.f_lineno, "call_date:  %s" % (call_date))
#    
#    # parse out set location
#    set_loc.append(loc_desc[i][loc_desc[i].find('(')+1:loc_desc[i].find(')')])
#    DebugPrint(__file__, frame.f_lineno, "set_loc:  %s" % ( loc_desc[i][loc_desc[i].find('(')+1:loc_desc[i].find(')')]))
#    
#
#    #extract call_time
#    hr_delta = 0
#    if ampm_re.search(days[i]):  # time formatting - into python datetime
#        hr_delta = 12
#    array = re.findall(r'[0-9]+', days[i]) 
#    DebugPrint(__file__, frame.f_lineno, "len(array):  %d" % ( len(array)))
#    DebugPrint(__file__, frame.f_lineno, "array:  %s" % (array))
#    if len(array) == 2:
#        call_time = (datetime.time(int(array[0])+hr_delta, int(array[1])))
#    else:
#        hour = int(array[0])
#        if (hour > 29):
#            hour = math.floor(hour/100)
#        if hour == 12:
#            hour -= 12
#        call_time = (datetime.time(hour+hr_delta, 0))
#    DebugPrint(__file__, frame.f_lineno, "call_time:  %s" % (call_time))
#
#    # set up the call and wrap datetime objects
#    date_object = datetime.datetime.strptime(call_date, output_format)
#    calltime_object = date_object.replace(hour = call_time.hour, minute = call_time.minute)
#    call.append(calltime_object)
#    wrap.append(call[i] + datetime.timedelta(hours = 13))
#    i += 1


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