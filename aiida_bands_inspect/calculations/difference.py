# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines a calculation to run the ``bands-inspect difference`` command.
"""

from fsc.export import export

from aiida import orm
from aiida.engine import CalcJob
from aiida.common import CalcInfo, CodeInfo

from ..io import write_bands


@export
class DifferenceCalculation(CalcJob):
    """
    Calculation class for the ``bands-inspect difference`` command.

    Arguments
    ---------
    bands1 : aiida.orm.nodes.data.array.bands.BandsData
        First band structure to compare.
    bands2 : aiida.orm.nodes.data.array.bands.BandsData
        Second band structure to compare.
    """

    _OUTPUT_FILE_NAME = 'diff.txt'

    @classmethod
    def define(cls, spec):
        super(DifferenceCalculation, cls).define(spec)

        spec.input(
            'bands1',
            valid_type=orm.BandsData,
            help='First bandstructure which is to be compared'
        )
        spec.input(
            'bands2',
            valid_type=orm.BandsData,
            help='Second bandstructure which is to be compared'
        )

        spec.input(
            'metadata.options.parser_name',
            valid_type=str,
            default='bands_inspect.difference'
        )

        spec.output('difference', valid_type=orm.Float)

        spec.exit_code(
            200,
            'ERROR_NO_RETRIEVED_FOLDER',
            message='The retrieved folder data node could not be accessed.'
        )
        spec.exit_code(
            210,
            'ERROR_OUTPUT_FILE_MISSING',
            message=
            'The retrieved folder does not contain the difference output file.'
        )

    def prepare_for_submission(self, tempfolder):  # pylint: disable=arguments-differ
        ev1_filename = 'eigenvals1.hdf5'
        ev2_filename = 'eigenvals2.hdf5'
        write_bands(self.inputs.bands1, tempfolder.get_abs_path(ev1_filename))
        write_bands(self.inputs.bands2, tempfolder.get_abs_path(ev2_filename))

        code = self.inputs.code

        calcinfo = CalcInfo()
        calcinfo.uuid = self.uuid
        calcinfo.remote_copy_list = []
        calcinfo.retrieve_list = [self._OUTPUT_FILE_NAME]

        codeinfo = CodeInfo()
        codeinfo.cmdline_params = ['difference', ev1_filename, ev2_filename]
        codeinfo.stdout_name = self._OUTPUT_FILE_NAME
        codeinfo.code_uuid = code.uuid
        calcinfo.codes_info = [codeinfo]

        return calcinfo
