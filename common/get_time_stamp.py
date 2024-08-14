import datetime
import time
import calendar


def get_today_start_stamp():
    today = datetime.date.today()

    str_date = today.strftime('%Y-%m-%d %H:%M:%S')  # 将日期转换为指定的显示格式
    start_time = time.strptime(str_date, "%Y-%m-%d %H:%M:%S")  # 将时间转化为数组形式
    #    print(pre_date)
    start_time_stamp = int(time.mktime(start_time))  # 将时间转化为时间戳形式
    return start_time_stamp


# 计算指定日期的前N天的时间戳
def get_pre_days_time_stamp(n):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    today_end_time_stamp = int(time.mktime(time.strptime(str(tomorrow), '%Y-%m-%d'))) - 1

    # 是今天的开始时间（00：00：00）
    today = datetime.date.today()
    pre_date = today - datetime.timedelta(days=n - 1)

    pre_date = pre_date.strftime('%Y-%m-%d %H:%M:%S')  # 将日期转换为指定的显示格式
    pre_time = time.strptime(pre_date, "%Y-%m-%d %H:%M:%S")  # 将时间转化为数组形式
    #    print(pre_date)
    pre_start_time_stamp = int(time.mktime(pre_time))  # 将时间转化为时间戳形式

    return pre_start_time_stamp, today_end_time_stamp


def get_pre_year_time_stamp():
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    date = datetime.datetime(year - 1, month + 1, 1)
    one_year_time_stamp = int(date.timestamp())

    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    today_end_time_stamp = int(time.mktime(time.strptime(str(tomorrow), '%Y-%m-%d'))) - 1
    return one_year_time_stamp, today_end_time_stamp


def get_total_time_stamp(start_ride_time_stamp):
    dt = datetime.datetime.fromtimestamp(start_ride_time_stamp)
    year = dt.year
    mouth = dt.month
    day = dt.day
    start_time_stamp = int(datetime.datetime(year, mouth, day).timestamp())

    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    today_end_time_stamp = int(time.mktime(time.strptime(str(tomorrow), '%Y-%m-%d'))) - 1
    return start_time_stamp, today_end_time_stamp


def get_month_last_day():
    now = datetime.datetime.now().date()
    this_month_end = datetime.datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1]).date()
    end_time_stamp = int(time.mktime(time.strptime(str(this_month_end + datetime.timedelta(days=1)), '%Y-%m-%d'))) - 1

    return end_time_stamp


if __name__ == '__main__':
    print(get_month_last_day())
