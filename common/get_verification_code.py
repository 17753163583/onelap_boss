import subprocess
import re


def get_verification_code():
    # 执行ADB命令打开短信APP
    sms_result = subprocess.run(['adb', 'shell',
                                 "content query --uri content://sms/inbox --projection body --where "
                                 "\"address='10686060100000340718'\" | tail -n 1"],
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                encoding='utf-8')
    # print(sms_result.stdout)

    match = re.search(r'您的验证码是:(\d+)', str(sms_result))

    if match:
        verification_code = match.group(1)
        # str类型的code
        return verification_code
    else:
        return None


if __name__ == '__main__':
    print(type(get_verification_code()))
