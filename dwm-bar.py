import subprocess
import time
import json
from datetime import datetime

def main():
    counter = 300
    zfsNameCooked = ""
    zfsPoolSizeAvailCooked = ""
    zfsPoolSizeUsedCooked = ""
    while True:
        if counter == 300:
            zfsNameRaw = subprocess.run(["zfs", "list", "-o", "name"],  stdout=subprocess.PIPE, encoding='utf-8')
            zfsNameCooked = zfsNameRaw.stdout.splitlines()[1]
            zfsPoolSizeAvailRaw = subprocess.run(["zfs", "list", "-o", "available"],  stdout=subprocess.PIPE, encoding='utf-8') 
            zfsPoolSizeAvailCooked = float(zfsPoolSizeAvailRaw.stdout.splitlines()[1][0:-1]) * 1.099511628
            zfsPoolSizeUsedRaw = subprocess.run(["zfs", "list", "-o", "used"],  stdout=subprocess.PIPE, encoding='utf-8') 
            zfsPoolSizeUsedCooked = float(zfsPoolSizeUsedRaw.stdout.splitlines()[1][0:-1]) * 1.099511628
            zfsTotal = round(zfsPoolSizeUsedCooked + zfsPoolSizeAvailCooked, 2)
            percent = round((zfsPoolSizeUsedCooked / zfsTotal) * 100, 1)
            counter = 0
        

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if counter % 5 or counter == 0:
            cpuTempRaw = subprocess.run(["sensors", "-j"], stdout=subprocess.PIPE, encoding='utf-8')
            cpuTempCooked = json.loads(cpuTempRaw.stdout)
            cpuLoadRaw = subprocess.run(['cat', '/proc/loadavg'], stdout=subprocess.PIPE, encoding='utf-8')
            cpuLoadCooked = ' '.join(cpuLoadRaw.stdout.split(' ')[0:3])
        if current_time[-2:] == '00' or counter == 0: 
            uptimeRaw = subprocess.run(['uptime', '-p'], stdout=subprocess.PIPE, encoding='utf-8')
            uptimeCooked = uptimeRaw.stdout[:-1]
            uptimeCooked = uptimeCooked.replace(' days, ', 'd ')
            uptimeCooked = uptimeCooked.replace(' days', 'd ')
            uptimeCooked = uptimeCooked.replace(' day,', 'd ')
            uptimeCooked = uptimeCooked.replace(' day', 'd ')
            uptimeCooked = uptimeCooked.replace(' hours, ', 'h ')
            uptimeCooked = uptimeCooked.replace(' hours', 'h ')
            uptimeCooked = uptimeCooked.replace(' hour, ', 'h ')
            uptimeCooked = uptimeCooked.replace(' hour ', 'h ')
            uptimeCooked = uptimeCooked.replace(' minutes', 'm')
            uptimeCooked = uptimeCooked.replace(' minute', 'm')
        
            if uptimeCooked[-1:] == ' ':
                uptimeCooked = uptimeCooked[:-1]

        subprocess.run(["xsetroot", "-name", f"{zfsNameCooked}: {round(zfsPoolSizeUsedCooked, 2)}TB / {str(zfsTotal)}TB ({percent}%) | {cpuLoadCooked} ({round(cpuTempCooked['k10temp-pci-00c3']['Tctl']['temp1_input'], 1 )} C) | {current_time} ({uptimeCooked})"])
        counter += 1
        time.sleep(1)
main()
