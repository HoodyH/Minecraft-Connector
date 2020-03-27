import json
from configurations.configurations import mc_rcon


class TitleCommand:

    def __init__(self, target, position, text, bold, italic, underlined, strikethrough, obfuscated, color):
        self.__target = target
        self.__position = position
        self.__text = text
        self.__bold = bold
        self.__italic = italic
        self.__underlined = underlined
        self.__strikethrough = strikethrough
        self.__obfuscated = obfuscated
        self.__color = color

    @property
    def target(self):
        return self.__target

    @property
    def position(self):
        return self.__position

    @property
    def text(self):
        return self.__text

    @property
    def bold(self):
        return self.__bold

    @property
    def italic(self):
        return self.__italic

    @property
    def underlined(self):
        return self.__underlined

    @property
    def strikethrough(self):
        return self.__strikethrough

    @property
    def obfuscated(self):
        return self.__obfuscated

    @property
    def color(self):
        return self.__color

    def title_json_command(self):
        command_dict = {
            'text': self.text,
            'bold': self.bold,
            'italic': self.italic,
            'underlined': self.underlined,
            'strikethrough': self.strikethrough,
            'obfuscated': self.obfuscated,
            'color': self.color,
        }
        return json.dumps(command_dict)

    def send(self):
        command = 'title {} {} {}'.format(
            self.target,
            self.position,
            self.title_json_command(),
        )
        mc_rcon.command(command)

    def reset(self):
        command = 'title {} {} {}'.format(
            self.target,
            self.position,
            '{"text": ""}',
        )
        mc_rcon.command(command)


class TitleCommandBuilder:
    def __init__(self):
        self.__target = None
        self.__position = None
        self.__text = None
        self.__bold = False
        self.__italic = False
        self.__underlined = False
        self.__strikethrough = False
        self.__obfuscated = False
        self.__color = None

    def targeting(self, value: str):
        self.__target = value
        return self

    def at_position(self, value):
        self.__position = value
        return self

    def with_text(self, value):
        self.__text = value
        return self

    def bold(self):
        self.__bold = True
        return self

    def italic(self):
        self.__italic = True
        return self

    def underlined(self):
        self.__underlined = True
        return self

    def strikethrough(self):
        self.__strikethrough = True
        return self

    def obfuscated(self):
        self.__obfuscated = True
        return self

    def with_color(self, value):
        self.__color = value
        return self

    def validate(self):
        return (self.__target is not None) and (self.__text is not None) and (self.__position is not None)

    def build(self):
        if self.validate():
            return TitleCommand(
                self.__target,
                self.__position,
                self.__text,
                self.__bold,
                self.__italic,
                self.__underlined,
                self.__strikethrough,
                self.__obfuscated,
                self.__color
            )
        else:
            raise ValueError
