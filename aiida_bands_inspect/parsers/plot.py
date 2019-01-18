# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

from fsc.export import export

from aiida.orm import DataFactory
from aiida.parsers.parser import Parser


@export
class PlotParser(Parser):
    """
    Parse bands_inspect plot_bands output to a 'singlefile' data.
    """

    def parse_with_retrieved(self, retrieved):
        try:
            out_folder = retrieved[self._calc._get_linkname_retrieved()]
        except KeyError as e:
            self.logger.error("No retrieved folder found")
            raise e

        res = DataFactory('singlefile')()
        res.add_path(out_folder.get_abs_path(self._calc._OUTPUT_FILE_NAME))

        new_nodes_list = [('plot', res)]

        return True, new_nodes_list
