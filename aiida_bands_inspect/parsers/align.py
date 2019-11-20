# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

from fsc.export import export

from aiida.plugins import DataFactory
from aiida.parsers.parser import Parser
from ..io import read_bands
from ..calculations.align import AlignCalculation


@export
class AlignParser(Parser):
    """
    Parse output of the align command: The shifted eigenvals files to
    BandsData objects, and the difference and shift values to Float.

    Returns
    -------
    bands1_shifted : aiida.orm.data.array.bands.BandsData
        Shifted band structure 1.
    bands2_shifted : aiida.orm.data.array.bands.BandsData
        Shifted band structure 2.
    shift: Float
        The value by which the two bandstructures were shifted in total.
    difference: Float
        The remaining difference between the two bandstructures.
    """
    def parse(self, **kwargs):  # pylint: disable=inconsistent-return-statements
        try:
            out_folder = self.retrieved
        except KeyError:
            return self.exit_codes.ERROR_NO_RETRIEVED_FOLDER

        try:
            with out_folder.open(
                AlignCalculation._EV1_SHIFTED_FILENAME,  # pylint: disable=protected-access
                'r+b'
            ) as ev1_shifted_file:
                self.out('bands1_shifted', read_bands(ev1_shifted_file))

            with out_folder.open(
                AlignCalculation._EV2_SHIFTED_FILENAME,  # pylint: disable=protected-access
                'r+b'
            ) as ev2_shifted_file:
                self.out('bands2_shifted', read_bands(ev2_shifted_file))

            with out_folder.open(
                AlignCalculation._OUTPUT_FILE_NAME,  # pylint: disable=protected-access
                'r'
            ) as file_handle:
                out_lines = file_handle.readlines()

        except FileNotFoundError:
            return self.exit_codes.ERROR_OUTPUT_FILE_MISSING

        Float = DataFactory('float')
        try:
            shift_line, diff_line = [line.split() for line in out_lines]
            assert shift_line[0] == 'Shift:'
            self.out('shift', Float(float(shift_line[1])))
            assert diff_line[0] == 'Difference:'
            self.out('difference', Float(float(diff_line[1])))
        except AssertionError:
            return self.exit_codes.ERROR_OUTPUT_FILE_WRONG
