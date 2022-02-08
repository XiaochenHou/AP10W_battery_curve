from datetime import datetime
import pandas as pd
import re

INTERVAL = 2
FILE_NAME = 'SN095A_办公'
level_regex = r'level: (\d+)'
time_regex = r'\d{2}\:\d{2}\:\d{2}'
with open('D:\putty_log\%s.log' % FILE_NAME, 'r') as file:
    data = file.read().replace('\n', '')
    time_list = re.findall(time_regex, data)
    battery_list = re.findall(level_regex, data)

combined_list = list(zip(time_list, battery_list))
curr_time = time_list[0]
curr_battery = battery_list[0]
new_time = [curr_time]
new_battery = [int(curr_battery)]
for index, tuples in enumerate(combined_list[1:]):
    if tuples[1] != curr_battery:
        curr_battery = tuples[1]
        new_time.append(tuples[0])
        new_battery.append(int(tuples[1]))
df = pd.DataFrame(list(zip(new_time, new_battery)), columns=['time', 'battery'])


def time_duration(str1, str2):
    datetime_object1 = datetime.strptime(str1, '%H:%M:%S')
    datetime_object2 = datetime.strptime(str2, '%H:%M:%S')
    return (datetime_object2 - datetime_object1).total_seconds()


time_diff = []
j = 1
while j <= len(new_time) - 1:
    time_diff.append(time_duration(new_time[j - 1], new_time[j]))
    j += 1

df['duration'] = pd.Series(time_diff)
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

result = pd.concat([df, df2], axis=1, join='outer')
result.to_excel(r'D:\\%s.xlsx' % FILE_NAME, index=False, header=True)
