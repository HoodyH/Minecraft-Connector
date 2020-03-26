from rcon_commd_builder.commands.title import TitleCommandBuilder
from rcon_commd_builder.utils.colors import Color
from rcon_commd_builder.utils.selectors import Selector
from rcon_commd_builder.utils.title_positions import TitlePosition

from time import sleep


class DrawTitles(object):

    def __init__(self):
        pass

    @staticmethod
    def __count_down(time, text):
        countdown = time
        countdown_builder = TitleCommandBuilder() \
            .targeting(Selector.ALL_PLAYERS) \
            .at_position(TitlePosition.TITLE) \
            .with_text(str(countdown)) \
            .with_color(Color.GOLD)

        countdown_builder.build().send()

        while countdown > 0:
            sleep(1)
            countdown_builder.with_text(str(countdown - 1))
            countdown_builder.build().send()
            countdown -= 1

        countdown_builder.with_text(text).build().send()

    def __start_screen(self):
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

        self.__count_down(3, 'GO!')
        subtitle_builder.with_text('Run For Your Life').build().send()

    def start_game(self):
        self.__start_screen()

    def game_over(self):
        self.__count_down(15, 'GAME OVER')
