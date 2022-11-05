import subprocess as sp


def thermal_charger_disable():
    sp.run(r'adb root')
    print('adb root')
    sp.run(r'adb remount')
    print('adb remount')
    sp.run(r'adb shell setprop sys.retaildemo.enabled 1')
    print('adb shell setprop sys.retaildemo.enabled 1')
    sp.run(r'adb shell setprop vendor.disable.usb.overheat.mitigation.control 1')
    print('adb shell setprop vendor.disable.usb.overheat.mitigation.control 1')
    sp.run(r'adb shell "echo disabled > /dev/thermal/tz-by-name/neutral_therm/mode"')
    print('adb shell "echo disabled > /dev/thermal/tz-by-name/neutral_therm/mode"')
    sp.run('adb shell cat /dev/thermal/tz-by-name/neutral_therm/mode')
    print('adb shell cat /dev/thermal/tz-by-name/neutral_therm/mode')
    sp.run(r'adb shell setprop persist.vendor.disable.thermal.control 1')
    print(r'adb shell setprop persist.vendor.disable.thermal.control 1')
    sp.run(r'adb shell stop vendor.thermal-hal-2-0')
    print(r'adb shell stop vendor.thermal-hal-2-0')
    sp.run(r'adb shell dumpsys battery set level 100')
    print(r'adb shell dumpsys battery set level 100')
    sp.run(r'adb shell mount -t debugfs debugfs /sys/kernel/debug')
    print(r'adb shell mount -t debugfs debugfs /sys/kernel/debug')
    sp.run(r'adb shell "echo 1 > /d/google_charger/input_suspend"')
    print(r'adb shell "echo 1 > /d/google_charger/input_suspend"')


def get_serial_devices():
    return sp.run(r'adb devices', capture_output=True).stdout.decode().split('\r\n')[1].split('\t')[0]

def reboot():
    sp.run(r'adb reboot')

def get_odpm_current(count=1):
    """
    Current unit is mA
    :return:
    """
    print('----------Get Current from ODPM----------')
    n = 0
    current = 0
    while n < count:
        temp = sp.run(r'adb shell pmic s2mpg14 getcurrent 36 | grep mA',
                      capture_output=True).stdout.decode().strip().split('=')[1]
        if eval(temp) > current:
            current = eval(temp)
        n += 1
    print(f'Get the ODPM current: {current} mA')
    return round(current, 2)

def main():
    pass
    # current = get_odpm_current()
    # print(current)


if __name__ == '__main__':
    main()