import subprocess as sp
import re
from time import sleep
import utils.parameters.external_paramters as ext_pmt

SHL = 'adb shell '
CAT = '"cat" '
CD = '/sys/bus/iio/devices/iio\:'
PMIC = 'device0/energy_value '
grep = '"| grep" '


# cat_cmd = SHL + CAT + CD + PMIC + grep


def record_current(count=10):
    rffe_rail = 25
    modem_rail = 23
    panel_rail = 19
    cpu1_rail = 9
    cpu2_rail = 7
    cpu3_rail = 5
    time = 1
    vol_typ = ext_pmt.vol_typ
    print(vol_typ)
    avg_count = count
    while True:
        rffe_ma_lst = []
        cpu_ma_lst = []
        modem_ma_lst = []
        panel_ma_lst = []
        for i in range(0, avg_count):
            get_pwr = sp.run(SHL + CAT + CD + PMIC, capture_output=True).stdout.decode()
            uwatta = re.split(', |\r\n|t=', get_pwr)
            sleep(0.1)
            get_pwr = sp.run(SHL + CAT + CD + PMIC, capture_output=True).stdout.decode()
            uwattb = re.split(', |\r\n|t=', get_pwr)

            time_msa = int(uwatta[time])
            rffe_uwa = int(uwatta[rffe_rail])
            # modem_uwa = int(uwatta[modem_rail])
            # panel_uwa = int(uwatta[panel_rail])
            # cpu_uwa = int(uwatta[cpu1_rail]) + int(uwatta[cpu2_rail]) + int(uwatta[cpu3_rail])

            time_msb = int(uwattb[time])
            rffe_uwb = int(uwattb[rffe_rail])
            # modem_uwb = int(uwattb[modem_rail])
            # panel_uwb = int(uwattb[panel_rail])
            # cpu_uwb = int(uwattb[cpu1_rail]) + int(uwattb[cpu2_rail]) + int(uwattb[cpu3_rail])

            time_ms = time_msb - time_msa
            # cpu_uw = cpu_uwb - cpu_uwa
            rffe_uw = rffe_uwb - rffe_uwa
            # modem_uw = modem_uwb - modem_uwa
            # panel_uw = panel_uwb - panel_uwa
            try:
                rffe_ma = rffe_uw / vol_typ / time_ms
                # cpu_ma = cpu_uw / vol_typ / time_ms
                # modem_ma = modem_uw / vol_typ / time_ms
                # panel_ma = panel_uw / vol_typ / time_ms
                rffe_ma_lst.append(rffe_ma)
                # cpu_ma_lst.append(cpu_ma)
                # modem_ma_lst.append(modem_ma)
                # panel_ma_lst.append(panel_ma)

            except:
                pass
        avg_rffe = round(sum(rffe_ma_lst) / len(rffe_ma_lst), 2)
        # avg_modem = round(sum(modem_ma_lst) / len(modem_ma_lst), 2)
        # avg_panel = round(sum(panel_ma_lst) / len(panel_ma_lst), 2)
        # avg_cpu = round(sum(cpu_ma_lst) / len(cpu_ma_lst), 2)
        print(f'Get the record current: {avg_rffe} mA')

        return avg_rffe


def thermal_charger_disable():
    sp.run(r'adb root')
    print('adb root')
    sp.run(r'adb remount')
    print('adb remount')
    sp.run(r'adb shell "echo 1 > /d/google_charger/input_suspend"')
    print('adb shell "echo 1 > /d/google_charger/input_suspend"')
    sp.run(r'adb shell "setprop persist.vendor.disable.thermal.control 1"')
    print('adb shell "setprop persist.vendor.disable.thermal.control 1"')
    sp.run(r'adb shell "setprop persist.vendor.disable.thermal.tj.control 1"')
    print('adb shell "setprop persist.vendor.disable.thermal.tj.control 1"')
    # sp.run(r'adb shell setprop sys.retaildemo.enabled 1')
    # print('adb shell setprop sys.retaildemo.enabled 1')
    # sp.run(r'adb shell setprop vendor.disable.usb.overheat.mitigation.control 1')
    # print('adb shell setprop vendor.disable.usb.overheat.mitigation.control 1')
    # sp.run(r'adb shell "echo disabled > /dev/thermal/tz-by-name/neutral_therm/mode"')
    # print('adb shell "echo disabled > /dev/thermal/tz-by-name/neutral_therm/mode"')
    # sp.run('adb shell cat /dev/thermal/tz-by-name/neutral_therm/mode')
    # print('adb shell cat /dev/thermal/tz-by-name/neutral_therm/mode')
    # sp.run(r'adb shell setprop persist.vendor.disable.thermal.control 1')
    # print(r'adb shell setprop persist.vendor.disable.thermal.control 1')
    # sp.run(r'adb shell stop vendor.thermal-hal-2-0')
    # print(r'adb shell stop vendor.thermal-hal-2-0')
    # sp.run(r'adb shell dumpsys battery set level 100')
    # print(r'adb shell dumpsys battery set level 100')
    # sp.run(r'adb shell mount -t debugfs debugfs /sys/kernel/debug')
    # print(r'adb shell mount -t debugfs debugfs /sys/kernel/debug')
    # sp.run(r'adb shell "echo 1 > /d/google_charger/input_suspend"')
    # print(r'adb shell "echo 1 > /d/google_charger/input_suspend"')
    # sp.run(r'adb shell setprop persist.vendor.disable.thermal.tj.control 1')
    # print(r'adb shell setprop setprop persist.vendor.disable.thermal.tj.control 1')
    # sp.run(r'adb shell "getprop gsm.version.baseband"')
    # print(r'adb shell "getprop gsm.version.baseband"')
    # sp.run(r'adb shell "getprop ro.vendor.build.fingerprint"')
    # print(r'adb shell "getprop ro.vendor.build.fingerprint"')
    #
    # sp.run(r'adb shell "echo 25000 > /dev/thermal/tz-by-name/BIG/emul_temp"')
    # print(r'adb shell "echo 25000 > /dev/thermal/tz-by-name/BIG/emul_temp"')
    # sp.run(r'adb shell "echo 25000 > /dev/thermal/tz-by-name/MID/emul_temp"')
    # print(r'adb shell "echo 25000 > /dev/thermal/tz-by-name/MID/emul_temp"')
    # sp.run(r'adb shell "echo 25000 > /dev/thermal/tz-by-name/LITTLE/emul_temp"')
    # print(r'adb shell "echo 25000 > /dev/thermal/tz-by-name/LITTLE/emul_temp"')


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
    # n = 0
    # current = 0
    # while n < count:
    #     temp = sp.run(r'adb shell pmic s2mpg14 getcurrent 36 | grep mA',
    #                   capture_output=True).stdout.decode().strip().split('=')[1]
    #     if eval(temp) > current:
    #         current = eval(temp)
    #     n += 1
    #     sleep(0.1)
    odpm_list = []
    n = 0
    while n < count:
        odpm_current = sp.run(r'adb shell pmic s2mpg14 getcurrent 36 | grep mA',
                      capture_output=True).stdout.decode().strip().split('=')[1]
        odpm_list.append(eval(odpm_current))
        sleep(0.1)
        n += 1
    current_average = sum(odpm_list) / len(odpm_list)
    print(f'Get the ODPM average current: {current_average} mA')
    return round(current_average, 2)


def main():
    record_current()
    # current = get_odpm_current()
    # print(current)


if __name__ == '__main__':
    main()
