"""
Demonstrate the use of a generator that indicates for each adjacent pair of events in 
access_log the number of seconds elapsed between them
"""

from datetime import datetime, timedelta
from time import sleep

# Comment in the following import to generate a fixed number of lines from log
# from itertools import islice


def get_data(infile):
    """
    Lazy function to get data line by line from access log and strips timestamp
    as follows:

    20/Feb/2021:15:06:44 -0800

    It breaks when there are no more lines to read in.
    """

    # Comment in the next three lines to display a fixed number of lines from log
    # (e.g., 10)
    # number_of_lines = 20
    # lines = islice(infile, number_of_lines)
    # line = next(lines)


    # Reads line by line of file (or chunks of lines) and extracts timestamp
    while True:

        timestamp = infile.readline().split('[')[1].split(']')[0]

        # Comment in the following line and comment out the above line to display
        # a fixed number of lines from log
        # timestamp = line.split('[')[1].split(']')[0]

        # Ends the loop when there is no more data to read in.
        if not timestamp:
            break

        yield timestamp

        # Comment in the following line to display a fixed number of lines from log
        # line = next(lines)


def convert_string_to_time(timestamp):
    """
    Converts string to appropriate aware datetime format, including time
    zones.
    """

    return datetime.strptime(timestamp, '%d/%b/%Y:%H:%M:%S %z')


def print_time_delta(difference):
    """Converts timedelta to string format. For negative time, timedelta reflects 
    it as -1 day plus total seconds.
    
    For example:
        timedelta(days=-1, seconds=86385)
        -15 seconds
    Convert negative time to reflect in consistent format.
    """

    seconds = difference.seconds
    days = difference.days
    hours = 0
    minutes = 0

    # If negative time, convert to appropriate format.
    if (days < 0):
        # timedelta stores as days and seconds so adjust total negative 
        # seconds from negative day (86,400 seconds)
        seconds = 86400 - seconds
        days = abs(days + 1)

        # Breakdown total seconds to respective hours, minutes and seconds
        while (seconds >= 60):
            if (seconds >= 3600):
                hours = seconds // 3600
                seconds -= (hours * 3600)
            elif (seconds >= 60):
                minutes, seconds = divmod(seconds, 60)
        
        if (days == 0):
            # If negative time is less than a day, print in similar format
            # as str(t) with '-' notation
            print(f'-{hours}:{minutes:02}:{seconds:02}')
        else:
            # Otherwise include the negative days as applicable (e.g., adjusted
            # for a day for conversion of seconds as noted above)
            print(f'-{days}:{hours}:{minutes:02}:{seconds:02}')
    else:
        print(' ' + str(difference))

        
def time_delta(gen):
    """Calculates time delta between two events."""
    time1 = convert_string_to_time(next(gen))
    time2 = convert_string_to_time(next(gen))

    while True:

        yield time2 - time1
        time1 = time2

        time2 = convert_string_to_time(next(gen))


def display():
    """
    Opens the access log to read in line by line and display time differential
    of sequential events.
    """

    filename = '/etc/httpd/logs/access_log'

    # Checks whether file exists. If not, porgram is aborted.
    try:
        with open(filename, 'r') as f:

            # Displays time differential for sequential events with 1/4 second delay
            # Ctr + C to abort/end
            for diff in time_delta(get_data(f)):
                print_time_delta(diff)
                sleep(.25)
                
    except FileNotFoundError:
        raise(SystemExit)(f"The {filename} file does not exist.")


if __name__ == '__main__':

    print("Time lapse of sequential events in format of DDD:HH:MM:SS:")

    display()