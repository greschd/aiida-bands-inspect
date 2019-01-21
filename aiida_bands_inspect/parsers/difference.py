# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

from fsc.export import export

from aiida.orm.data.base import Float
from aiida.parsers.parser import Parser


@export
class DifferenceParser(Parser):
    """
    Parse ``bands_inspect difference`` output to float.

    Returns
    -------
    difference : aiida.orm.data.base.Float
        The calculated average difference.
    """

    def parse_with_retrieved(self, retrieved):
        try:
            out_folder = retrieved[self._calc._get_linkname_retrieved()]
        except KeyError as e:
            self.logger.error("No retrieved folder found")
            raise e

        with open(
            out_folder.get_abs_path(self._calc._OUTPUT_FILE_NAME), 'r'
        ) as f:
            res = float(f.read())

        new_nodes_list = [('difference', Float(res))]

        return True, new_nodes_list
