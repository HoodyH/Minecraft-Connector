from mcpi.minecraft import Minecraft
from mcrcon import MCRcon


BOT_NAME = '<Pavlov>'
SERVER_IP = '10.32.10.112'
PASSWORD = 'superrconpassword'

mc = Minecraft.create(SERVER_IP)
mc_rcon = MCRcon(SERVER_IP, PASSWORD)
