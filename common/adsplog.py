import subprocess
import sys
import json
from datetime import datetime

class AdspLog:

    def __init__(self, folder):
        self.base_folder = folder
        today = datetime.today()
        self.folder = '{}/{}/{}/{}/{}'.format(folder, today.year, today.month, today.day, today.hour)


    def getLastLine(self):
        cmd = 'find %s -type f -mmin -1' % self.folder
        #proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

        stdout = []
        with subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL) as proc:
            read = proc.stdout.read()
            if read:
                files = read.decode('utf-8').splitlines()
                stdout.extend(files)

        # exclude debug.log
        for f in stdout:
            if 'debug.log' in f:
                stdout.remove(f)

        if proc.returncode > 0 or len(stdout) == 0:
            raise Exception("Find process did not find a log file or a permission problem ocurred.")

        lines = None
        last_line = None
        filename = stdout.pop()
        with open(filename, 'r') as f:
            lines = f.readlines()
        if lines:
            last_line = lines.pop()

        return last_line


    def getDeviceIds(self, line):
        columns = line.split(',', 13)
        data = json.loads(columns.pop(), encoding='utf-8')
        if 'deviceIds' in data.keys():
            return data['deviceIds']
        return None

