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
    difference : aiida.orm.data.base.Float
        The calculated average difference.
    """
    def parse(self, **kwargs):
        try:
            out_folder = self.retrieved
        except KeyError as e:
            self.logger.error("No retrieved folder found")
            raise e

        with out_folder.open(
            DifferenceCalculation._OUTPUT_FILE_NAME, 'r'
        ) as f:
            res = float(f.read())

        self.out('difference', Float(res))
