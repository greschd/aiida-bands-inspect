# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

from fsc.export import export

from aiida.orm import Float
from aiida.parsers.parser import Parser

from ..calculations.difference import DifferenceCalculation


@export
class DifferenceParser(Parser):
    """
    Parse ``bands_inspect difference`` output to float.

    Returns
    -------
    difference : aiida.orm.nodes.data.float.Float
        The calculated average difference.
    """
    def parse(self, **kwargs):  # pylint: disable=inconsistent-return-statements
        try:
            out_folder = self.retrieved
        except KeyError:
            return self.exit_codes.ERROR_NO_RETRIEVED_FOLDER

        try:
            with out_folder.open(
                DifferenceCalculation._OUTPUT_FILE_NAME,  # pylint: disable=protected-access
                'r'
            ) as f:
                res = float(f.read())
        except IOError:
            return self.exit_codes.ERROR_OUTPUT_FILE_MISSING

        self.out('difference', Float(res))
