import datetime

dates = [
    "2020-07-22 23:27:33.322841",
    "2020-07-01 23:29:04.104892",
    "2020-07-15 23:29:10.371306",
    "2020-07-21 23:30:01.312357",
    "2020-07-21 23:30:44.298923"
    ]


#print(sorted(dates))

for item in sorted(dates):
    cut_days_and_time = item.split(' ')
    del cut_days_and_time[1]
    result = datetime.datetime(cut_days_and_time[0])
    print(result)
        