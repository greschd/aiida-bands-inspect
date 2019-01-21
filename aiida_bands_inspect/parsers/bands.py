# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

from fsc.export import export

from aiida.orm import DataFactory
from aiida.parsers.parser import Parser
from ..io import read_bands


@export
class BandsParser(Parser):
    """
    Parse bands_inspect eigenvals file to a BandsData object.

    Returns
    -------
    bands : aiida.orm.data.array.bands.BandsData
        Retrieved band structure.
    """

    def parse_with_retrieved(self, retrieved):
        try:
            out_folder = retrieved[self._calc._get_linkname_retrieved()]
        except KeyError:
            self.logger.error("No retrieved folder found")

        bands_file = out_folder.get_abs_path(self._calc._OUTPUT_FILE_NAME)
        new_nodes_list = [('bands', read_bands(bands_file))]

        return True, new_nodes_list
