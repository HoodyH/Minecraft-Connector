from time import sleep
from mcpi.minecraft import Minecraft
from mcrcon import MCRcon
from core.minecraft_ids import *

server_ip = '10.32.10.112'
rcon_password = 'superrconpassword'

server_username = '<Pavlov>'


items = [
    MinecraftItem(IRON_SWORD).id_string+Enchant([
        (Enchant.UNBREAKING, 3),
        (Enchant.SHARPNESS, 2),
    ]).enchantments_string,

    MinecraftItem(IRON_HELMET).id_string+Enchant([
        (Enchant.UNBREAKING, 3),
    ]).enchantments_string,

    MinecraftItem(IRON_CHESTPLATE).id_string+Enchant([
        (Enchant.UNBREAKING, 3),
    ]).enchantments_string,

    MinecraftItem(IRON_LEGGINGS).id_string+Enchant([
        (Enchant.UNBREAKING, 3),
    ]).enchantments_string,

    MinecraftItem(IRON_BOOTS).id_string+Enchant([
        (Enchant.UNBREAKING, 3),
    ]).enchantments_string,

    MinecraftItem(BOW).id_string+Enchant([
        (Enchant.UNBREAKING, 3),
        (Enchant.INFINITY, 3),
    ]).enchantments_string,

    MinecraftItem(ARROW).id_string+Enchant([
        (Enchant.UNBREAKING, 3),
    ]).enchantments_string,

    MinecraftItem(CROSSBOW).id_string+Enchant([
        (Enchant.UNBREAKING, 3),
        (Enchant.INFINITY, 3),
    ]).enchantments_string,

    MinecraftItem(GOLDEN_CARROT).id_string,
]

temp_players = {}


def main():

    mc = Minecraft.create(server_ip)
    mcr = MCRcon(server_ip, rcon_password)

    while True:
        chat_events = mc.events.pollChatPosts()
        if chat_events:
            for chat_event in chat_events:

                mex = chat_event.message
                entity_id = chat_event.entityId

                log = 'LOG: Mex:"{}" from:"{}"'.format(
                    mex,
                    entity_id,
                )
                print(log)

                if mex.startswith('.addplayer'):
                    name = mex[11:]
                    try:
                        id_check = mc.getPlayerEntityId(name)
                        temp_players[id_check] = name
                        mc.postToChat('{} {} added, now you can use the commands .help for info'.format(
                            server_username,
                            name
                        ))
                        print(temp_players)

                    except Exception as e:
                        print('EXCEPTION: {}'.format(e))
                        if len(name) <= 1:
                            mc.postToChat('{} your name is missing'.format(server_username))
                        else:
                            mc.postToChat('{} {} not found'.format(server_username, name))

                if mex == '.weapons':
                    mcr.connect()
                    player = temp_players.get(entity_id)
                    if player:
                        for item in items:
                            c = 'give {} {} {}'.format(player, item, 1)
                            mcr.command(c)
                    else:
                        mc.postToChat(
                            '{} player not in rcon command system, usa .addplayer "player_name" to add'.format(
                                server_username,
                            )
                        )
                    mcr.disconnect()

                if mex == '.help':
                    mcr.connect()
                    msg_add_player = '\u00A76.addplayer "player_name"\u00A7f --> to allow user to use commands'
                    msg_weapons = '\u00A76.weapons\u00A7f --> get a set of weapons to fight in hungergames arena'

                    msgs_help_list = [
                        msg_add_player,
                        msg_weapons
                    ]

                    mcr.command('say \u00A7cList of commands:')
                    for msg in msgs_help_list:
                        mcr.command('say {}'.format(msg))
                    mcr.disconnect()

        sleep(1)


if __name__ == "__main__":
    main()
