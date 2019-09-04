# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

from fsc.export import export

from aiida.plugins import DataFactory
from aiida.parsers.parser import Parser

from ..calculations.plot import PlotCalculation


@export
class PlotParser(Parser):
    """
    Parse ``bands-inspect plot_bands`` output to a 'singlefile' data.

    Returns
    -------
    plot : aiida.orm.data.singlefile.SinglefileData
        File containing the generated plot.
    """

    def parse(self, **kwargs):
        try:
            out_folder = self.retrieved
        except KeyError as e:
            self.logger.error("No retrieved folder found")
            raise e

        with out_folder.open(
            PlotCalculation._OUTPUT_FILE_NAME, 'rb'
        ) as handle:
            self.out('plot', DataFactory('singlefile')(file=handle))
