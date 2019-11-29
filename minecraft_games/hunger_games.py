from minecraft_core.commands.title import TitleCommandBuilder
from minecraft_core.utils.colors import Color
from minecraft_core.utils.selectors import Selector
from minecraft_core.utils.title_positions import TitlePosition

from time import sleep


class HungerGames(object):

    def __init__(self):
        pass

    @staticmethod
    def start_screen():
        title = TitleCommandBuilder() \
            .targeting(Selector.ALL_PLAYERS) \
            .at_position(TitlePosition.TITLE) \
            .with_text('Hunger Games') \
            .with_color(Color.RED) \
            .build()
        title.send()

        subtitle_builder = TitleCommandBuilder() \
            .targeting(Selector.ALL_PLAYERS) \
            .at_position(TitlePosition.SUBTITLE) \
            .with_text('Triggerati Edition')\
            .italic() \
            .with_color(Color.DARK_RED)

        subtitle = subtitle_builder.build()
        subtitle.send()
        sleep(4)
        subtitle.reset()

        countdown = 3
        countdown_builder = TitleCommandBuilder() \
            .targeting(Selector.ALL_PLAYERS) \
            .at_position(TitlePosition.TITLE) \
            .with_text(str(countdown)) \
            .with_color(Color.GOLD)

        countdown_builder.build().send()

        while countdown > 0:
            sleep(1)
            countdown_builder.with_text(str(countdown-1))
            countdown_builder.build().send()
            countdown -= 1

        countdown_builder.with_text('GO!').build().send()
        subtitle_builder.with_text('Run For Your Life').build().send()

    def start_game(self):
        self.start_screen()
