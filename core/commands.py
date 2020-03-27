from configurations.configurations import mc_rcon, mc, BOT_NAME
from commands.dig.dig import Dig
from commands.hunger_games.hunger_games import HungerGames


class Commands:

    def __init__(self):
        self.mc = mc
        self.mcr = mc_rcon

        self.dig = Dig()
        self.hunger_games = HungerGames()

    def check_commands(self):
        chat_events = self.mc.events.pollChatPosts()
        if chat_events:

            self.mcr.connect()
            for chat_event in chat_events:

                mex = chat_event.message
                entity_id = chat_event.entityId

                log = 'LOG: Mex:"{}" from:"{}"'.format(
                    mex,
                    entity_id,
                )
                print(log)

                if mex.startswith('.disconnect'):
                    self.mcr.disconnect()
                    self.mc.postToChat('{} mrc disconnected'.format(BOT_NAME))
                    return

                """
                Enable the automatic walking excavation
                """
                if mex.startswith('.mine'):
                    self.dig.active_status = not self.dig.active_status
                    self.mc.postToChat('{} auto mining toggled to {}'.format(
                        BOT_NAME,
                        self.dig.active_status,
                    ))
                    return

                """
                Add a player in the system for the target commands
                """
                if mex.startswith('.join'):
                    name = mex[6:]
                    try:
                        id_check = self.mc.getPlayerEntityId(name)
                        self.hunger_games.add_player(id_check, name)
                        self.mc.postToChat('{} {} added, now you can use the commands .help for info'.format(
                            BOT_NAME,
                            name
                        ))

                    except Exception as e:
                        print('EXCEPTION: {}'.format(e))
                        if len(name) <= 1:
                            self.mc.postToChat('{} your name is missing'.format(BOT_NAME))
                        else:
                            self.mc.postToChat('{} {} not found'.format(BOT_NAME, name))
                    return

                """
                Choose the team of player and set his spawn point to the selected team
                """
                if mex.startswith('.team'):
                    color = mex[5:].lower().replace(' ', '')
                    try:
                        self.hunger_games.set_team(entity_id, color.upper())
                        self.mc.postToChat('{} Team set to {}'.format(BOT_NAME, color.title()))
                        return
                    except ValueError as exc:
                        if str(exc) == 'Player Not Found':
                            self.mc.postToChat(
                                '{} Player not in rcon command system, use .join "player_name" to add'.format(
                                    BOT_NAME,
                                )
                            )
                        if str(exc) == 'Color Not Found':
                            self.mc.postToChat('{} Color not found'.format(BOT_NAME))
                    except Exception as exc:
                        if exc:
                            self.mc.postToChat('{} The game is started, you can\'t change team'.format(BOT_NAME))

                """
                Start a game with a time
                """
                if mex.startswith('.start'):
                    try:
                        self.hunger_games.start()
                        self.mc.postToChat('{} Let\'s the games begin'.format(BOT_NAME))
                    except Exception as exc:
                        print(exc)
                        if exc:
                            self.mc.postToChat('{} The game is started, you can\'t start a new game'.format(BOT_NAME))

                """
                Teleport all the players to the lobby
                """
                if mex.startswith('.lobby'):
                    self.hunger_games.all_to_lobby()
                    self.mc.postToChat('{} Prepare for the battle'.format(BOT_NAME))

                """
                length of the game
                """
                if mex.startswith('.gametime'):
                    try:
                        time = int(mex[10:].replace(' ', ''))
                    except ValueError:
                        self.mc.postToChat('{} Wrong value try with a number'.format(BOT_NAME))
                        return
                    self.hunger_games.game_time = time
                    self.mc.postToChat('{} Game time set to {}'.format(BOT_NAME, time))

                """
                Give to a specific player the items contained in self.items,
                the container is statically built
                """
                if mex == '.weapons':
                    try:
                        self.hunger_games.weapons(entity_id)
                    except ValueError:
                        self.mc.postToChat(
                            '{} player not in rcon command system, usa .join "player_name" to add'.format(
                                BOT_NAME,
                            )
                        )

                """
                Send in minecraft game chat the list of available commands
                """
                if mex == '.help':
                    msg_add_player = '\u00A76.join "player_name"\u00A7f --> to allow user to use commands'
                    msg_weapons = '\u00A76.weapons\u00A7f --> get a set of weapons to fight in hungergames arena'
                    msg_team = '\u00A76.team "color"\u00A7f --> ' \
                               'teleport the player and set his spawn point for selected team\n' \
                               '\u00A79Colors: white orange blue yellow green grey'
                    msg_start = '\u00A76.stat\u00A7f --> Once ready start the game'
                    msg_lobby = '\u00A76.lobby\u00A7f --> Teleport players to the lobby'
                    msg_game_time = '\u00A76.gametime\u00A7f --> Duration of a game in minutes'

                    msgs_help_list = [
                        msg_add_player,
                        msg_weapons,
                        msg_team,
                        msg_start,
                        msg_lobby,
                        msg_game_time
                    ]

                    self.mcr.command('say \u00A7cList of commands:')
                    for msg in msgs_help_list:
                        self.mcr.command('say {}'.format(msg))

    def do_looped_actions(self):
        self.dig.mining()
