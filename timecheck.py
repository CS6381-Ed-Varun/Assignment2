import datetime

#time_started = datetime.time
time_started = (datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()

#print(time_started.strftime("%H:%M:%S.%f"))
print(time_started)