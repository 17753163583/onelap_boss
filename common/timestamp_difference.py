from datetime import datetime, timedelta

timestamp1 = 1638186000  # 第一个时间戳
timestamp2 = 1638189000  # 第二个时间戳


def time_stamp_diff(start_time_stamp, end_time_stamp):
    # 将时间戳转换为datetime对象
    dt1 = datetime.fromtimestamp(start_time_stamp)
    dt2 = datetime.fromtimestamp(end_time_stamp)

    # 计算两个datetime对象之间的时间差
    time_diff = dt2 - dt1

    # 提取分钟数、秒数和毫秒数
    minutes = time_diff.total_seconds() // 60
    seconds = time_diff.total_seconds() % 60
    milliseconds = time_diff.total_seconds() * 1000 % 1000

    print("相差分钟数:", minutes)
    print("相差秒数:", seconds)
    print("相差毫秒数:", milliseconds)


if __name__ == '__main__':
    time_stamp_diff(1720420862, 1783492862)
