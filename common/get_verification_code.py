import subprocess
import re


def get_verification_code():
    phone = 106934450000340719
    adb = f"adb shell content query --uri content://sms/inbox --projection body --where address='{phone}'"
    sms_result = subprocess.check_output(adb).decode('utf-8')

    print(sms_result)

    match = re.search(r'您的验证码是:(\d+)', str(sms_result))

    if match:
        verification_code = match.group(1)
        # str类型的code
        return verification_code
    else:
        return None


if __name__ == '__main__':
    # adb shell content query --uri content://sms/inbox --projection body --where address='106934450000340719'
    print(get_verification_code())
