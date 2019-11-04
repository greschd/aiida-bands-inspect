# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines the a calculation class for the ``bands-inspect plot`` command.
"""

from fsc.export import export

from aiida import orm
from aiida.engine import CalcJob
from aiida.common import CalcInfo, CodeInfo

from ..io import write_bands


@export
class PlotCalculation(CalcJob):
    """
    Calculation class for the ``bands_inspect plot`` command.

    Arguments
    ---------
    bands1 : aiida.orm.nodes.data.array.bands.BandsData
        First band structure to plot.
    bands2 : aiida.orm.nodes.data.array.bands.BandsData
        Second band structure to plot.
    """

    _OUTPUT_FILE_NAME = 'plot.pdf'

    @classmethod
    def define(cls, spec):
        super(PlotCalculation, cls).define(spec)

        spec.input(
            'bands1',
            valid_type=orm.BandsData,
            help="First bandstructure which is to be plotted"
        )
        spec.input(
            'bands2',
            valid_type=orm.BandsData,
            help="Second bandstructure which is to be plotted"
        )

        spec.input(
            'metadata.options.parser_name',
            valid_type=str,
            default='bands_inspect.plot'
        )

        spec.output(
            'plot',
            valid_type=orm.SinglefileData,
            help='The created band-structure comparison plot.'
        )

        spec.exit_code(
            200,
            'ERROR_NO_RETRIEVED_FOLDER',
            message='The retrieved folder data node could not be accessed.'
        )
        spec.exit_code(
            210,
            'ERROR_OUTPUT_FILE_MISSING',
            message='The retrieved folder does not contain the plot output file.'
        )

    def prepare_for_submission(self, tempfolder):  # pylint: disable=arguments-differ
        ev1_filename = 'eigenvals1.hdf5'
        ev2_filename = 'eigenvals2.hdf5'
        eigenval_file_1 = tempfolder.get_abs_path(ev1_filename)
        write_bands(self.inputs.bands1, eigenval_file_1)
        eigenval_file_2 = tempfolder.get_abs_path(ev2_filename)
        write_bands(self.inputs.bands2, eigenval_file_2)

        calcinfo = CalcInfo()
        calcinfo.uuid = self.uuid
        calcinfo.remote_copy_list = []
        calcinfo.retrieve_list = [self._OUTPUT_FILE_NAME]

        codeinfo = CodeInfo()
        codeinfo.cmdline_params = ['plot-bands', ev1_filename, ev2_filename]
        codeinfo.code_uuid = self.inputs.code.uuid
        calcinfo.codes_info = [codeinfo]

        return calcinfo
