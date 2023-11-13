import RV8803

gps_time = None

rtc = RV8803.RV_8803()

print(rtc.getFullTime())

rtc.setHours(gps_time["hours"])
rtc.setMinutes(gps_time["minutes"])
rtc.setSeconds(gps_time["Seconds"])

rtc.setDate(gps_time["day"])
rtc.setMonth(gps_time["month"])
rtc.setYear(gps_time["year"])
