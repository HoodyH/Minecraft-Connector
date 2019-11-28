import os
import subprocess
from time import sleep
import tarfile
from datetime import datetime
from threading import Timer
import logging
import sys

log_name = 'logs/minecraft-connector.log'
file_handler = logging.FileHandler(filename=log_name)
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=handlers
)

logger = logging.getLogger('MCLOG')
logging.info('Log_name: {}'.format(log_name))


class MinecraftServerExecutableBuilder:
    def __init__(self, minecraft_server=None, max_ram=4096, startup_ram=1024):
        self.__minecraft_server = minecraft_server
        self.__max_ram = max_ram
        self.__startup_ram = startup_ram

    def build_executable_string(self):
        out = 'java -Xmx{}m -Xms{}m -jar '.format(self.max_ram, self.startup_ram)
        out += '{}/'
        out += self.minecraft_server
        return out

    @property
    def minecraft_server(self):
        return self.__minecraft_server

    @minecraft_server.setter
    def minecraft_server(self, value):
        self.__minecraft_server = value

    @property
    def max_ram(self):
        return self.__max_ram

    @max_ram.setter
    def max_ram(self, value):
        self.__max_ram = value

    @property
    def startup_ram(self):
        return self.__startup_ram

    @startup_ram.setter
    def startup_ram(self, value):
        self.__startup_ram = value


class MinecraftServerHandler:

    def __init__(self, minecraft_dir, executable_string, backup_dir='/backup'):

        self.minecraft_dir = minecraft_dir
        self.backup_dir = backup_dir
        self.executable_string = executable_string.format(minecraft_dir)
        self.exclude_file = "plugins/dynmap"
        self.process = None

    @staticmethod
    def server_command(self, cmd):
        logging.info('Writing server command')
        self.process.stdin.write(str.encode('{}\n'.format(cmd)))  # just write the command to the input stream
        self.process.stdin.flush()

    def start_server(self):
        os.chdir(self.minecraft_dir)
        logging.info('Starting server')
        self.process = subprocess.Popen(self.executable_string, stdin=subprocess.PIPE)
        logging.info("Server started.")

    def start_backup(self):
        logging.info('Starting backup timer')
        try:
            timer = Timer(self.next_backup_time(), self.backup)  # FIND NEXT HOURLY MARK
            timer.start()  # START BACKUP FOR THEN
            logging.info('Timer started')
        except Exception as e:
            logging.info('{}'.format(e), exc_info=True)
            os.popen('TASKKILL /PID ' + str(self.process.pid) + ' /F')

    def filter_function(self, tarinfo):
        if tarinfo.name != self.exclude_file:
            logging.info(tarinfo.name, "ADDED")
            return tarinfo

    def make_tarfile(self, output_filename, source_dir):
        logging.info('Making tarfile')
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir), filter=self.filter_function)

    def backup(self):
        global t
        self.server_command("say Backup starting. World no longer saving...")
        self.server_command("save-off")
        self.server_command("save-all")
        sleep(3)
        os.chdir(self.backup_dir)
        logging.info('Deleting last file')
        try:
            os.remove("%s\\minecraft-hour24.tar.gz" % self.backup_dir)
        except:
            pass

        logging.info('Renaming old files')
        for i in range(24, 0, -1):
            try:
                os.rename(
                    "%s\\minecraft-hour%s.tar.gz" % (self.backup_dir, i-1),
                    "%s\\minecraft-hour%s.tar.gz" % (self.backup_dir, i)
                )
            except:
                pass
        self.make_tarfile("%s\\minecraft-hour0.tar.gz" % self.backup_dir, self.minecraft_dir+"/")
        self.server_command("save-on")
        self.server_command("say Backup complete. World now saving.")
        logging.info('Starting new timer')
        try:
            t = Timer(self.next_backup_time(), self.backup)  # FIND NEXT HOURLY MARK
            t.start()  # START BACKUP FOR THEN
            logging.info('New timer started')
        except:
            logging.info('', exc_info=True)
            os.popen('TASKKILL /PID '+str(self.process.pid)+' /F')

    def next_backup_time(self):
        logging.info('Calculating next time')
        x = datetime.today()
        if x.hour != 23:
            y = x.replace(hour=x.hour+1, minute=0, second=0, microsecond=0)
        else:
            try:
                y = x.replace(day=x.day+1, hour=0, minute=0, second=0, microsecond=0)
            except:
                try:
                    y = x.replace(month=x.month+1, day=1, hour=0, minute=0, second=0, microsecond=0)
                except:
                    try:
                        y = x.replace(year=x.year+1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
                    except:
                        logging.info('I, the backup script, have no idea what time it is in an hour.', exc_info=True)
                        os.popen('TASKKILL /PID '+str(self.process.pid)+' /F')
        logging.info('Next backup time is %s' % y)
        delta_t = y-x
        secs = delta_t.seconds+1
        return secs
