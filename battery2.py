import pathlib
from datetime import datetime
import pandas as pd
import re
import argparse
import time
import os

"""                                                                                                   
     █████ ███████████ █████       █████ █████ ███████████ ██████████ █████   ████
    ░░███ ░░███░░░░░░█░░███       ░░███ ░░███ ░█░░░███░░░█░░███░░░░░█░░███   ███░ 
     ░███  ░███   █ ░  ░███        ░░███ ███  ░   ░███  ░  ░███  █ ░  ░███  ███   
     ░███  ░███████    ░███         ░░█████       ░███     ░██████    ░███████    
     ░███  ░███░░░█    ░███          ░░███        ░███     ░███░░█    ░███░░███   
     ░███  ░███  ░     ░███      █    ░███        ░███     ░███ ░   █ ░███ ░░███  
     █████ █████       ███████████    █████       █████    ██████████ █████ ░░████
    ░░░░░ ░░░░░       ░░░░░░░░░░░    ░░░░░       ░░░░░    ░░░░░░░░░░ ░░░░░   ░░░░                                                                                                                                                                                                                                                                                                                                                    
"""


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


def main(file_dir, dest_dir=None):
    """
    The main function that is effective for creating the Excel format worksheet
    :param file_dir: The directory/path to the file
    :param dest_dir: The directory/path to the destination
    :return: Nothing, just in case it is not a valid format file and end the function as quick as possible.
    """
    # regular expressions for the levels and time need to be extracted from the log
    if file_dir[-4:] != '.log' and file_dir[-4:] != '.txt':
        print("ERROR! The input log must be ended with '.log' or '.txt'!")
        print()
        return
    start = time.time()
    level_regex = r'level: (\d+)'
    time_regex = r'\d{2}\:\d{2}\:\d{2}'
    with open(file_dir, 'r') as file:
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
    if dest_dir:
        result.to_excel(dest_dir, index=False, header=True)
    else:
        result.to_excel(file_dir[:-3] + "xlsx", index=False, header=True)
    end = time.time()
    print(f'========Successfully processed in {round(end - start, 2)}s!========')
    print()


parser = argparse.ArgumentParser(description="Process the battery log file and output some useful sheets")
parser.add_argument('f', type=str, help="The input log file/folder with path")
parser.add_argument('-p', type=str, metavar="Destination path", help="The optional output path")
parser.add_argument('-i', type=int, metavar="Time Interval", default=2,
                    help="The optional time interval setting, default is 2")
args = parser.parse_args()
INTERVAL = args.i

# recognise whether the input arguments are valid
if args.p:
    if args.d[-5:] != ".xlsx":
        raise TypeError("The destination file must be ended with '.xlsx'!")

if os.path.isdir(args.f):
    print("It is a directory")
    print("====================================")
    for path in pathlib.Path(args.f).iterdir():
        if path.is_file():
            path_str = str(path)
            if "/" in path_str:
                file_name = path_str.split("/")[-1]
            else:
                file_name = path_str.split("\\")[-1]
            print(f"Processing the file: '{file_name}'")
            main(str(path))
elif os.path.isfile(args.f):
    print("It is a normal file")
    main(args.f, dest_dir=args.p)
else:
    raise TypeError("The input log must be ended with '.log' or '.txt' or a directory!")
