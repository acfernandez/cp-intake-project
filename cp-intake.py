import json
from collections import Counter

# TODO read files from directory
files = ['4f7bb24040f4c49b_2023-08-25T19_41_13Z.json',
        'f4b9d653a6d02df8_2023-08-28T13_49_06Z.json',
        '3a8f4c90a9691256_2023-08-28T13_49_23Z.json', 
        '1c148e8fb21781c9_2023-08-28T12_12_53Z.json',
        '91883880558947dd_2023-08-28T12_12_53Z.json', 
        'a5fe379f46abdc5f_2023-08-29T13_38_51Z.json',
        'aecbfa94287a9df4_2023-08-29T14_44_56Z.json',
        '33a18af66f233887_2023-08-29T14_48_57Z.json',
        'f9e1a4d574ec9521_2023-08-29T15_06_19Z.json',
        '87258e6f71d68cea_2023-08-29T15_09_53Z.json']

devices = []
so_versions = []
battery_status = []

app_usage_dic = {}
app_usage_off_count = 0

app_installed_dic = {}
app_installed_off_count = 0

for file in files:
    f = open(file)
    data = json.load(f)
 
    devices.append(data['deviceInfo']['brand'])
    so_versions.append(data['deviceInfo']['releaseVersion'])
    battery_status.append(data['deviceInfo']['batteryStatus'])
    
    # TODO refact to method
    app_usage_full_list = data['appUsage']
    if app_usage_full_list:
        for value in app_usage_full_list:
            appName = value['appName']
            usage = value['usage']
            if appName in app_usage_dic:
                app_usage_dic[appName].append(usage)
            else:
                app_usage_dic[appName] = [usage] 
    else:
        app_usage_off_count += 1

    # TODO refact to method
    app_installed_full_list = data['installedAppsInfo']
    if app_installed_full_list:
        for value in app_installed_full_list:
            appName = value['appName']
            category = value['category']
            if appName in app_installed_dic:
                app_installed_dic[appName].append(category)
            else:
                app_installed_dic[appName] = [category]
    else:
        app_installed_off_count += 1

    f.close

print('- count android versions: ', dict(Counter(so_versions)))
print('- count devices brand: ', dict(Counter(devices)))
print('- count battery status: ', dict(Counter(battery_status)))
print('- count devices with usage permission off: ', app_usage_off_count)
print('- count devices without apps installed: ', app_installed_off_count)

app_usage_summarized_list = []

for item in app_usage_dic.items():
    app_usage_summarized_list.append( (item[0], sum(item[1])) )

app_usage_summarized_list.sort(key = lambda x:x[1], reverse=True)
print('- apps ordered by usage time in seconds: ')
[print (item) for item in app_usage_summarized_list]


app_installed_summarized_list = []
app_category_installed_list = []

for item in app_installed_dic.items():
    app_installed_summarized_list.append( (item[0], len(item[1])) )
    for i in item[1]: app_category_installed_list.append( i )

app_installed_summarized_list.sort(key = lambda x:x[1], reverse=True)
print('- apps ordered by installed times: ')
[print (i) for i in app_installed_summarized_list]

print('- count apps categories installed: ')
print(dict(Counter(app_category_installed_list)))