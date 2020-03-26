from time import sleep
from core.commands import Commands
from core.ServerHandler import (MinecraftServerHandler, MinecraftServerExecutableBuilder)


def server():

    executable_string = MinecraftServerExecutableBuilder('spigot_1.14.4.jar').build_executable_string()
    handler = MinecraftServerHandler('/babango', executable_string)
    # handler.server_start()
    # sleep(80)  # wait for the server start
    handler.start_backup()

    cmd = Commands()
    while True:
        cmd.check_commands()
        cmd.do_looped_actions()
        sleep(0.25)


def main():
    server()


if __name__ == "__main__":
    main()
