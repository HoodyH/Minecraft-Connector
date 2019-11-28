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

logger = logging.getLogger('mc_log')
logging.info('Log Destination File: {}'.format(log_name))
