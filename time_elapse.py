"""
Demonstrate the use of a generator that indicates for each adjacent pair of events in 
access_log the number of seconds elapsed between them
"""

from datetime import datetime, timedelta
from time import sleep


def get_data(infile):
    """
    Lazy function to get data line by line from access log and strips timestamp
    as follows:

    20/Feb/2021:15:06:44 -0800

    It breaks when there are no more lines to read in.
    """

    index = 0
    # lines = islice(infile, 5)
    # line = next(lines)

    # Reads line by line of file and extracts timestamp
    while True:

        timestamp = infile.readline().split('[')[1].split(']')[0]
        # print(f'index {index}: {timestamp}')
        
        # Ends the loop when there is no more data to read in.
        if not timestamp:
            break

        yield timestamp
    


def convert_string_to_time(timestamp):
    """Converts string to appropriate aware datetime format."""

    return datetime.strptime(timestamp, '%d/%b/%Y:%H:%M:%S %z')


def print_time_delta(difference):
    """Converts timedelta to string format."""
    seconds = difference.seconds
    hours = 0
    minutes = 0

    while (seconds >= 60):
        if (seconds >= 3600):
            hours = seconds // 3600
            seconds -= (hours * 3600)
        elif (seconds >= 60):
            minutes, seconds = divmod(seconds, 60)

    print(f'{difference.days:03}:{hours:02}:{minutes:02}:{seconds:02}')

        
def time_delta(gen):
    """Calculates time delta between two events."""
    # count = 1
    time1 = convert_string_to_time(next(gen))
    time2 = convert_string_to_time(next(gen))
    # count += 1

    while True:
        # print(time1)
        # print(time2)
        # print(f'count: {count}')

        yield time2 - time1
        time1 = time2

        try:
            time2 = convert_string_to_time(next(gen))
            # count += 1
        except:
            break


def display():
    """
    Opens the file designated by user and performs lazy read of file in
    batches of 80 characters. For each batch, it is passed onto the produce(gen)
    function to properly ensure that words are not cut off within the 
    80-character limit and prints out each modified line.
    """

# for x in (line.split('[')[1].split(']')[0] for line in itertools.islice(open('/etc/httpd/logs/access_log'), 0, 500)):

    filename = '/etc/httpd/logs/access_log'

    # Checks whether file exists. If not, porgram is aborted.
    try:
        with open(filename, 'r') as f:

            # Displays time differential for sequential events with 1 second delay
            # Ctr + C to abort/end
            for diff in time_delta(get_data(f)):
                print_time_delta(diff)
                sleep(1)
                
    except FileNotFoundError:
        raise(SystemExit)(f"The {filename} file does not exist.")


if __name__ == '__main__':

    print("Time lapse of sequential events in format of DDD:HH:MM:SS:")

    display()