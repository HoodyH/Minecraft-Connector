from time import sleep
from mcpi.minecraft import Minecraft
from mcrcon import MCRcon
from core.commands import Commands
from core.ServerHandler import (MinecraftServerHandler, MinecraftServerExecutableBuilder)

from minecraft_games.hunger_games import HungerGames


server_ip = '10.32.10.112'
rcon_password = 'superrconpassword'


def server():
    mc = Minecraft.create(server_ip)
    mcr = MCRcon(server_ip, rcon_password)

    executable_string = MinecraftServerExecutableBuilder('spigot_1.14.4.jar').build_executable_string()
    handler = MinecraftServerHandler('/babango', executable_string)
    # handler.server_start()
    # sleep(80)  # wait for the server start
    handler.start_backup()

    cmd = Commands(mc, mcr)

    while True:
        cmd.check_commands()
        cmd.do_looped_actions()
        sleep(0.25)


def main():
    hg = HungerGames()
    hg.start_game()


if __name__ == "__main__":
    main()
