# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

from aiida.parsers.parser import Parser
from ..io import read

__all__ = ('BandsParser', )


class BandsParser(Parser):
    """
    Parse bands_inspect eigenvals file to a BandsData object.

    Returns
    -------
    bands : aiida.orm.nodes.data.array.bands.BandsData
        Retrieved band structure.
    """
    def parse(self, **kwargs):  # pylint: disable=inconsistent-return-statements
        try:
            out_folder = self.retrieved
        except KeyError:
            self.logger.error("No retrieved folder found")

        result_filename = self.node.get_option('result_filename')
        # For compatibility with aiida-tbmodels <= 0.3
        if result_filename is None:
            result_filename = self.node.get_option('output_filename')
        try:
            with out_folder.open(result_filename, 'rb') as out_file:
                self.out('bands', read(out_file))
        except IOError:
            return self.exit_codes.ERROR_RESULT_FILE
