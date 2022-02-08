from datetime import datetime
import pandas as pd
import re
import argparse

parser = argparse.ArgumentParser(description="Process the battery log file and output some useful sheets")
parser.add_argument('log_file_dir', type=str, help="The input log name with path")
parser.add_argument('-d', type=str, metavar="Destination directory", help="The optional output directory")
args = parser.parse_args()

if args.log_file_dir[-4:] != '.log' and args.log_file_dir[-4:] != '.txt':
    raise TypeError("The input log must be ended with '.log' or '.txt'!")
if args.d:
    if args.d[-5:] != ".xlsx":
        raise TypeError("The destination file must be ended with '.xlsx'!")

INTERVAL = 2
FILE_NAME = args.log_file_dir.split("\\")[-1].split(".")[0]

# regular expressions for the levels and time need to be extracted from the log
level_regex = r'level: (\d+)'
time_regex = r'\d{2}\:\d{2}\:\d{2}'


def time_duration(time_start, time_end):
    """
    This function is used to calculate the time difference in seconds.
    :param time_start: The start time represented by a string.
    :param time_end: The end time represented by a string.
    :return: The time difference in seconds, integer representation.
    """
    datetime_object1 = datetime.strptime(time_start, '%H:%M:%S')
    datetime_object2 = datetime.strptime(time_end, '%H:%M:%S')
    return (datetime_object2 - datetime_object1).total_seconds()


with open(args.log_file_dir, 'r') as file:
    data = file.read().replace('\n', '')
    # find the all the time and all the battery levels and put them in lists
    time_list = re.findall(time_regex, data)
    battery_list = re.findall(level_regex, data)

combined_list = list(zip(time_list, battery_list))
curr_time = time_list[0]
curr_battery = battery_list[0]
new_time = [curr_time]
new_battery = [int(curr_battery)]
# the first two columns, calculated by the difference of the battery levels
for index, tuples in enumerate(combined_list[1:]):
    if tuples[1] != curr_battery:
        curr_battery = tuples[1]
        new_time.append(tuples[0])
        new_battery.append(int(tuples[1]))
df = pd.DataFrame(list(zip(new_time, new_battery)), columns=['time', 'battery'])

time_diff = []
j = 1
while j <= len(new_time) - 1:
    time_diff.append(time_duration(new_time[j - 1], new_time[j]))
    j += 1

df['duration'] = pd.Series(time_diff)

# add two empty columns to separate two types of calculations
df['empty1'] = pd.Series(dtype=float)
df['empty2'] = pd.Series(dtype=float)

time_index = 0
battery_index = 0
time2 = []
battery2 = []
while time_index < len(time_list):
    time2.append(time_list[time_index])
    time_index += int(60 / INTERVAL)
while battery_index < len(battery_list):
    battery2.append(int(battery_list[battery_index]))
    battery_index += int(60 / INTERVAL)
df2 = pd.DataFrame(list(zip(time2, battery2)), columns=['time', 'battery'])

# outer join the two data frames
result = pd.concat([df, df2], axis=1, join='outer')
# output the file in Excel
if args.d:
    result.to_excel(args.d, index=False, header=True)
else:
    result.to_excel(args.log_file_dir[:-3] + "xlsx", index=False, header=True)
