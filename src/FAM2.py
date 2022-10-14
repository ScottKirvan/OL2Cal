
import re 
from DBPrint import DebugPrint 
import inspect
import datetime

frame = inspect.currentframe()

def Process(events, line = []):
    #days_re = re.compile(r'^DAY |^DOUBLE ') # todo - need a better regex - specify start of line
    days_re = re.compile(r'Estimated ') # todo - need a better regex - specify start of line
    ampm_re = re.compile(r'pm') # todo - need a better regex - specify end of line 
    endday_re = re.compile(r'End Day # ') # todo - need a better regex - specify start of line
    locdesc_re = re.compile(r'Int |Ext |INT') # todo - need a better regex

    # dig through and find the "important info" for each shooting day
    i = 0
    days = []
    loc_desc = []
    end_day = []
    DebugPrint(__file__, frame.f_lineno, "len(line): (%d)" % (len(line)))
    while i < len(line):
        if days_re.search(line[i]):  # find the "Estimated Crew Call" line
            hr_delta = 0
            days.append(line[i]) # this has our call time (call)
            DebugPrint(__file__, frame.f_lineno, "days:  %s" % (line[i]))
            while i < len(line) and not locdesc_re.search(line[i]):
                i += 1
            loc_desc.append(line[i]) # this has our script location (set_loc)
            DebugPrint(__file__, frame.f_lineno, "loc_desc:  %s" % (line[i]))
            while i < len(line) and not endday_re.search(line[i]):
                i += 1
            end_day.append(line[i]) # this has our day number (day_num) and call date (call_date)
            DebugPrint(__file__, frame.f_lineno, "end_day: (%d) %s" % (i, line[i]))
        i += 1

    # %%
    # from that "important info", extract actual details that we want to import to gcal
    i = 0
    call_date = [] # temp var
    day_num = []
    set_loc = []
    calltime_object = [] # includes date - temp var
    call = []
    wrap = []
    DebugPrint(__file__, frame.f_lineno, "%d days" % (len(days)))
    while i < len(days):
        # extract all the numbers we need to process the Day line (day, call time)
        array = re.findall(r'[0-9]+', end_day[i]) 

        # parse out day number (day_num)
        DebugPrint(__file__, frame.f_lineno, "day_num:  %s" % (array[0]))
        day_num.append(array[0])

        DebugPrint(__file__, frame.f_lineno, "array:  %s" % (array))

        # parse out call date (call_date)
        matches = re.findall(
            r'((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d+,\s+\d+)',
            end_day[i])
        input_format = "%B %d, %Y" # full month name, day and year
        output_format = "%m/%d/%Y"
        for match in matches:
            new_date = datetime.datetime.strptime(match, input_format).strftime(output_format)
            call_date = new_date
        DebugPrint(__file__, frame.f_lineno, "call_date:  %s" % (call_date))
        
        # parse out set location
        set_loc.append(loc_desc[i][loc_desc[i].find('(')+1:loc_desc[i].find(')')])
        DebugPrint(__file__, frame.f_lineno, "set_loc:  %s" % ( loc_desc[i][loc_desc[i].find('(')+1:loc_desc[i].find(')')]))
        

        #extract call_time
        hr_delta = 0
        if ampm_re.search(days[i]):  # time formatting - into python datetime
            hr_delta = 12
        array = re.findall(r'[0-9]+', days[i]) 
        DebugPrint(__file__, frame.f_lineno, "len(array):  %d" % ( len(array)))
        DebugPrint(__file__, frame.f_lineno, "array:  %s" % (array))
        if len(array) == 2:
            call_time = (datetime.time(int(array[0])+hr_delta, int(array[1])))
        else:
            hour = int(array[0])
            if (hour > 29):
                hour = math.floor(hour/100)
            if hour == 12:
                hour -= 12
            call_time = (datetime.time(hour+hr_delta, 0))
        DebugPrint(__file__, frame.f_lineno, "call_time:  %s" % (call_time))

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