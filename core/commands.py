from core.minecraft_ids import *
from core.dig import Dig

server_username = '<Pavlov>'


class Commands:

    sword_enchant = Enchant([(Enchant.UNBREAKING, 3), (Enchant.SHARPNESS, 2)]).enchantments_string
    unbreaking_enchant = Enchant([(Enchant.UNBREAKING, 3)]).enchantments_string
    bow_enchant = Enchant([(Enchant.UNBREAKING, 3), (Enchant.INFINITY, 3)]).enchantments_string
    boot_enchant = Enchant([(Enchant.UNBREAKING, 3), (Enchant.FEATHER_FALLING, 2)]).enchantments_string

    items = [
        MinecraftItem(IRON_SWORD, enchant=sword_enchant).id_string,
        MinecraftItem(BOW, enchant=bow_enchant).id_string,
        MinecraftItem(GOLDEN_CARROT, quantity=64).id_string,
        MinecraftItem(CROSSBOW, enchant=unbreaking_enchant).id_string,
        MinecraftItem(FLINT_AND_STEEL).id_string,
        MinecraftItem(IRON_HELMET, enchant=unbreaking_enchant).id_string,
        MinecraftItem(IRON_CHESTPLATE, enchant=unbreaking_enchant).id_string,
        MinecraftItem(IRON_LEGGINGS, enchant=unbreaking_enchant).id_string,
        MinecraftItem(IRON_BOOTS, enchant=boot_enchant).id_string,
        MinecraftItem(ARROW, quantity=64).id_string,
    ]

    teams = {
        'white': '-51 63 263',
        'orange': '-58 63 192',
        'blue': '6 63 180',
        'yellow': '61 63 202',
        'green': '86 63 255',
        'grey': '23 63 276',
    }

    def __init__(self, mc, mcr):
        self.mc = mc
        self.mcr = mcr

        self.temp_players = {}

        self.dig = Dig(mc, mcr)

    def check_commands(self):
        chat_events = self.mc.events.pollChatPosts()
        if chat_events:
            for chat_event in chat_events:

                mex = chat_event.message
                entity_id = chat_event.entityId

                log = 'LOG: Mex:"{}" from:"{}"'.format(
                    mex,
                    entity_id,
                )
                print(log)

                """
                Enable the automatic walking excavation
                """
                if mex.startswith('.mine'):
                    self.dig.active_status = not self.dig.active_status
                    self.mc.postToChat('{} auto mining toggled to {}'.format(
                        server_username,
                        self.dig.active_status,
                    ))

                """
                Add a player in the system for the target commands
                """
                if mex.startswith('.addplayer'):
                    name = mex[11:]
                    try:
                        id_check = self.mc.getPlayerEntityId(name)
                        self.temp_players[id_check] = name
                        self.mc.postToChat('{} {} added, now you can use the commands .help for info'.format(
                            server_username,
                            name
                        ))
                        print(self.temp_players)

                    except Exception as e:
                        print('EXCEPTION: {}'.format(e))
                        if len(name) <= 1:
                            self.mc.postToChat('{} your name is missing'.format(server_username))
                        else:
                            self.mc.postToChat('{} {} not found'.format(server_username, name))

                """
                Teleport the player and set his spawn point to the selected team
                """
                if mex.startswith('.team'):
                    color = mex[5:].lower().replace(' ', '')
                    print('1'+color+'1')
                    coords = self.teams.get(color)
                    print(coords)
                    if not coords:
                        self.mc.postToChat('{} {} not found'.format(server_username, color))
                        return

                    self.mcr.connect()
                    player = self.temp_players.get(entity_id)
                    if player:
                        c = 'teleport {} {}'.format(player, coords)
                        self.mcr.command(c)
                        c = 'spawnpoint {} {}'.format(player, coords)
                        self.mcr.command(c)
                    else:
                        self.mc.postToChat(
                            '{} player not in rcon command system, usa .addplayer "player_name" to add'.format(
                                server_username,
                            )
                        )
                    self.mcr.disconnect()

                """
                Give to a specific player the items contained in self.items,
                the container is statically built
                """
                if mex == '.weapons':
                    self.mcr.connect()
                    player = self.temp_players.get(entity_id)
                    if player:
                        for item in self.items:
                            c = 'give {} {}'.format(player, item)
                            res = self.mcr.command(c)
                            print(res)
                    else:
                        self.mc.postToChat(
                            '{} player not in rcon command system, usa .addplayer "player_name" to add'.format(
                                server_username,
                            )
                        )
                    self.mcr.disconnect()

                """
                Send in minecraft game chat the list of available commands
                """
                if mex == '.help':
                    self.mcr.connect()
                    msg_add_player = '\u00A76.addplayer "player_name"\u00A7f --> to allow user to use commands'
                    msg_weapons = '\u00A76.weapons\u00A7f --> get a set of weapons to fight in hungergames arena'
                    msg_team = '\u00A76.team "color"\u00A7f --> ' \
                               'teleport the player and set his spawn point for selected team\n' \
                               '\u00A79Colors: white orange blue yellow green grey'

                    msgs_help_list = [
                        msg_add_player,
                        msg_weapons,
                        msg_team,
                    ]

                    self.mcr.command('say \u00A7cList of commands:')
                    for msg in msgs_help_list:
                        self.mcr.command('say {}'.format(msg))
                    self.mcr.disconnect()

    def do_looped_actions(self):
        self.dig.mining()
