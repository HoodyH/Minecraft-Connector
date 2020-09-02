from random import  randrange
from threading import Timer
from configurations.configurations import mc_rcon
from core.minecraft_ids import *
from .modules.player import Player
from .modules.teams import Teams
from .modules.titles import DrawTitles


class HungerGames:

    def __init__(self):
        self.mcr = mc_rcon
        self.dt = DrawTitles()
        self.lobby = []

        self.__is_game = False
        self.game_time = 10
        self.max_deaths = 10

        self.game_timer = None

        self.teams = [
            'WHITE',
            'ORANGE',
            'BLUE',
            'YELLOW',
            'GREEN',
            'GREY',
        ]

    def __find_player(self, player_id):
        player: Player
        for player in self.lobby:
            if player.player_id == player_id:
                return player
        else:
            return None

    def add_player(self, player_id, name):
        if not self.__find_player(player_id):
            p = Player(player_id, name)

            idx = randrange(0, len(self.teams))
            p.team = Teams[self.teams[idx]]

            self.lobby.append(p)
            # self.mcr.command('gamemode spectator {}'.format(name))
            self.mcr.command('gamemode survival {}'.format(name))
            return str(p.team)[6:].lower()

        return None

    def set_team(self, player_id: int, color):

        if self.__is_game:
            raise Exception('Game Already Started')

        try:
            team = Teams[color]
        except Exception as exc:
            raise ValueError('Color Not Found')

        player = self.__find_player(player_id)
        if not player:
            raise ValueError('Player Not Found')

        player.team = team

    def weapons(self, player_id):

        player = self.__find_player(player_id)
        if not player:
            raise ValueError('Player Not Found')

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

        for item in items:
            self.mcr.command('give {} {}'.format(player.name, item))

    def all_to_lobby(self):

        self.__is_game = False

        for player in self.lobby:
            self.mcr.command('teleport {} {}'.format(player.name, Teams.LOBBY.value))
            self.mcr.command('gamemode survival {}'.format(player.name))
            self.mcr.command('clear {}'.format(player.name))
        self.mcr.command('scoreboard objectives setdisplay list Kills')
        self.mcr.command('team modify pvp friendlyFire false')

    def start(self):

        if self.__is_game:
            raise Exception('Game Already Started')

        self.__is_game = True

        self.mcr.command('scoreboard objectives add Deaths deathCount')
        self.mcr.command('scoreboard objectives add Kills playerKillCount')
        self.mcr.command('scoreboard objectives add Health health')

        self.mcr.command('scoreboard objectives setdisplay list Health')
        self.mcr.command('time set night')

        for player in self.lobby:
            self.mcr.command('spawnpoint {} {}'.format(player.name, player.team.value))
            self.mcr.command('teleport {} {}'.format(player.name, player.team.value))
            self.mcr.command('gamemode survival {}'.format(player.name))
            self.mcr.command('scoreboard players reset {} Deaths'.format(player.name))
            self.mcr.command('scoreboard players reset {} Kills'.format(player.name))

        # Print to screen
        self.dt.start_game()
        self.mcr.command('team modify pvp friendlyFire true')

        # give the weapons to all the players
        for player in self.lobby:
            self.weapons(player.player_id)

        self.game_timer = Timer(self.game_time * 60, self.end_game)
        self.game_timer.start()

    def check_status(self):

        if not self.__is_game:
            return

        player: Player
        for player in self.lobby:
            out = self.mcr.command('scoreboard players get {} Deaths'.format(player.name))
            try:
                counter = int(out[out.find('has') + 4:out.find('[') - 1])
            except ValueError:
                counter = 0

            if counter >= self.max_deaths and self.__is_game is True:
                self.mcr.command('gamemode spectator {}'.format(player.name))

    def end_game(self):
        self.dt.game_over()
        self.all_to_lobby()
