import datetime



#时间日期转换为时间戳格式
date_str = '2024-10-12'
# 将日期字符串转换为 datetime 对象
date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
# 设置时间为 23:59:59
end_of_day = date_obj.replace(hour=23, minute=59, second=59)
# 将 datetime 对象转换为秒级时间戳
timestamp_seconds = end_of_day.timestamp()
# 转换为毫秒级别时间戳
timestamp_milliseconds = int(timestamp_seconds * 1000)
print("要求回货时间对应时间戳为:", timestamp_milliseconds)