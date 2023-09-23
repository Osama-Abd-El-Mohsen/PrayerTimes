from PrayerTimes import remanning_time,index,salat,json_not_state
import win11toast
import datetime

if json_not_state == True:
    now = datetime.datetime.now()
    now_hour = int(now.strftime("%H"))
    now_min = int(now.strftime("%M"))
    current_time = now.strftime("%H:%M")

    next_hours, next_min = remanning_time.split(':')

    remanning_time = (datetime.timedelta(
        hours=int(next_hours), minutes=int(30)) - datetime.timedelta(hours=now_hour, minutes=now_min))

    rem_hour, rem_min, rem_sec = str(remanning_time).split(':')

    if next_hours == now_hour and next_min == now_min:

        win11toast.toast('حان الأن موعد أذان', f'{salat[index]}')


    elif rem_min == '05' :
        win11toast.toast(' متبقى 5 دقائق على اذان', f'{salat[index]}')
