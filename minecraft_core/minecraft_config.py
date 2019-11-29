import logging
import sys
from mcpi.minecraft import Minecraft
from mcrcon import MCRcon

"""
Minecraft server Information
To connect over Rcon and over PiMinecraft
"""
server_ip = '10.32.10.112'
rcon_password = 'superrconpassword'

mc = Minecraft.create(server_ip)
mc_rcon = MCRcon(server_ip, rcon_password)


"""
Logger Information
Remember to create the file in the right directory or the program will not start.
"""
log_name = 'logs/minecraft-connector.log'
file_handler = logging.FileHandler(filename=log_name)
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=handlers
)

logger = logging.getLogger('mc_log')
logging.info('Log Destination File: {}'.format(log_name))
