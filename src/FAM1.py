
import re 
from DBPrint import DebugPrint 
import inspect
import datetime

frame = inspect.currentframe()

def Process(events, line = []):
    days_re = re.compile(r'\* Day') # todo - need a better regex - specify start of line
    ampm_re = re.compile(r'pm \*') # todo - need a better regex - specify end of line 
    endday_re = re.compile(r'End Day # ') # todo - need a better regex - specify start of line

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

    events.days = days
    events.day_num = day_num
    events.set_loc = set_loc
    events.call = call
    events.wrap = wrap