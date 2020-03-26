from .teams import Teams


class Player:
    def __init__(self, player_id, name):
        self.player_id = player_id
        self.name = name
        self.team = Teams.LOBBY
        self.kills = 0
        self.deaths = 0
