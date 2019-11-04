# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

from fsc.export import export

from aiida.parsers.parser import Parser
from ..io import read_bands


@export
class BandsParser(Parser):
    """
    Parse bands_inspect eigenvals file to a BandsData object.

    Returns
    -------
    bands : aiida.orm.nodes.data.array.bands.BandsData
        Retrieved band structure.
    """
    def parse(self, **kwargs):
        try:
            out_folder = self.retrieved
        except KeyError:
            self.logger.error("No retrieved folder found")

        with out_folder.open(
            self.node.get_option('output_filename'), 'r+b'
        ) as out_file:
            self.out('bands', read_bands(out_file))
