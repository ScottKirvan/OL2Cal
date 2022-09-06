# processes one liner pdf into a google calendar csv file
# %%
#import requests ## not used - for http requests, so you could grab a pdf file via url
import re
import pdfplumber
#from datetime import time
import datetime
import argparse
import os

# These are the different regex patterns that are used to find specific lines and details - these may need tweaking based on 
# changes in the oneliner.  I think I'd like to see things like this moved to a config file

days_re = re.compile(r'\* Day') # todo - need a better regex - specify start of line
ampm_re = re.compile(r'pm \*') # todo - need a better regex - specify end of line 
endday_re = re.compile(r'End Day # ') # todo - need a better regex - specify start of line


# %%
# command line parser
  
parser = argparse.ArgumentParser(description ='Process one-liner into Google Calendar CSV')
  
parser.add_argument(dest = "infile", metavar ='infile', nargs = 1, help = 'input filename (pdf)')
#parser.add_argument('-p', '--pat', metavar ='pattern', 
#                    required = True, dest ='patterns', 
#                    action ='append', 
#                    help ='text pattern to search for')
  
parser.add_argument('-v', dest ='verbose',
                    action ='store_true', help ='verbose mode')
parser.add_argument('-o', dest ='outfile', 
                    action ='store', help ='output file')
parser.add_argument('--speed', dest ='speed', 
                    action ='store', choices = {'slow', 'fast'},
                    default ='slow', help ='search speed')
args = parser.parse_args()

print("infile", args.infile[0])
print("verbose", args.verbose)
print("outfile", args.outfile)
print("speed", args.speed)
#print("filename", os.path.basename(args.infile[0]))
#exit()
# %%
# grab the pdf as text

oneliner = args.infile[0]

text=''
with pdfplumber.open(oneliner) as pdf:
    for page in pdf.pages:
        text += page.extract_text() + '\n'

# %%
# break that text into an array of lines
line = []
for line_tmp in text.split('\n'):
    line.append(line_tmp)

# %%
# dig through and find the important info for each shooting day
i = 0
days = []
loc_desc = []
end_day = []
while i < len(line):
    if days_re.search(line[i]):  # find the line that starts with "* Day"
        hr_delta = 0
        days.append(line[i])
        s = line[i+1]  # this next line will contain the location (first set location and story location)
        loc_desc.append(s)  #this is the full location line - story and set
        while i < len(line) and not endday_re.search(line[i]):
            i += 1
        end_day.append(line[i])
    i += 1


# %%
# from that "important info", extract actual details that we want to import to gcal
i = 0
call_date = []
day_num = []
set_loc = []
calltime_object = [] # includes date
call = []
wrap = []
while i < len(days):
    # extract all the numbers we need to process the Day line (day, call time)
    array = re.findall(r'[0-9]+', days[i]) 

    # extract day number
    day_num.append(array[0])

    #extract call_time
    hr_delta = 0
    if ampm_re.search(days[i]):  # time formatting - into python datetime
        hr_delta = 12
    if len(array) == 3:
        call_time = (datetime.time(int(array[1])+hr_delta, int(array[2])))
    else:
        hour = int(array[1])
        if hour == 12: 
            hour -= 12
        call_time = (datetime.time(hour+hr_delta, 0))

    # extract set location
    set_loc.append(loc_desc[i][loc_desc[i].find('(')+1:loc_desc[i].find(')')])
    
    # parse out call date
    matches = re.findall(
        r'((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d+,\s+\d+)',
        end_day[i])
    input_format = "%B %d, %Y" # full month name, day and year
    output_format = "%m/%d/%Y"
    for match in matches:
        new_date = datetime.datetime.strptime(match, input_format).strftime(output_format)
        call_date = new_date
    
    # set up the call and wrap datetime objects
    date_object = datetime.datetime.strptime(call_date, output_format)
    calltime_object = date_object.replace(hour = call_time.hour, minute = call_time.minute)
    call.append(calltime_object)
    wrap.append(call[i] + datetime.timedelta(hours = 13))
    i += 1


# %%
# format and output the data
# todo - put in code to escape all commas in strings
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
print (row)

i = 0
while i < len(days):
    Subject = "Day " + str(day_num[i]) + " - " + str(set_loc[i])
    #Start_Date = str(call_date[i])
    Start_Date = str(call[i].strftime("%m/%d/%Y"))
    Start_Time = (call[i].strftime("%I:%M %p"))
    All_day_event = "FALSE"
    End_Date = str(wrap[i].strftime("%m/%d/%Y"))
    End_Time = (wrap[i].strftime("%I:%M %p"))
    Location = str(set_loc[i])
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
    print (row)
    i += 1

# eof