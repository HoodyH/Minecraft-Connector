from mcpi import block


class Dig:

    def __init__(self, mc, mcr):
        self.mc = mc
        self.mcr = mcr

        self.__active = False

    def mining(self):

        if self.active_status:

            x_offset, y_max, z_offset = 1, 0, 1  # laterale, altezza da posizione player, profondita

            raw_x, raw_y, raw_z = self.mc.player.getPos()
            x, y, z = int(raw_x), int(raw_y), int(raw_z)

            for idx_x in range(x-x_offset, x+x_offset):
                for idx_y in range(y-1, y + y_max):
                    for idx_z in range(z - z_offset, z + z_offset):
                        self.mc.setBlock(idx_x, idx_y, idx_z, block.SAND.id)

    @property
    def active_status(self):
        return self.__active

    @active_status.setter
    def active_status(self, value):
        self.__active = value
