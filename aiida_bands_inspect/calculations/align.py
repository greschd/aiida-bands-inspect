# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines a calculation to run the ``bands-inspect align`` command.
"""

import six

from fsc.export import export

from aiida.engine import CalcJob
from aiida.common import CalcInfo, CodeInfo
from aiida.plugins import DataFactory

from ..io import write_bands


@export
class AlignCalculation(CalcJob):
    """
    Calculation class for the ``bands-inspect align`` command.

    Arguments
    ---------
    bands1 : aiida.orm.data.array.bands.BandsData
        First band structure to compare.
    bands2 : aiida.orm.data.array.bands.BandsData
        Second band structure to compare.
    """

    _OUTPUT_FILE_NAME = 'out.txt'

    _EV1_SHIFTED_FILENAME = 'eigenvals1_shifted.hdf5'
    _EV2_SHIFTED_FILENAME = 'eigenvals2_shifted.hdf5'

    @classmethod
    def define(cls, spec):
        super(AlignCalculation, cls).define(spec)
        BandsData = DataFactory('array.bands')

        spec.input(
            'bands1',
            valid_type=BandsData,
            help='First bandstructure which is to be aligned'
        )
        spec.input(
            'bands2',
            valid_type=BandsData,
            help='Second bandstructure which is to be aligned'
        )

        spec.input(
            'metadata.options.parser_name',
            valid_type=six.string_types,
            default='bands_inspect.align'
        )

        Float = DataFactory('float')
        spec.output('difference', valid_type=Float)
        spec.output('shift', valid_type=Float)
        spec.output('bands1_shifted', valid_type=BandsData)
        spec.output('bands2_shifted', valid_type=BandsData)

        spec.exit_code(
            200,
            'ERROR_NO_RETRIEVED_FOLDER',
            message='The retrieved folder data node could not be accessed.'
        )
        spec.exit_code(
            210,
            'ERROR_OUTPUT_FILE_MISSING',
            message=
            'At least one of the expected output files is missing from the retrieved folder.'
        )
        spec.exit_code(
            220,
            'ERROR_OUTPUT_FILE_WRONG',
            message='The text output file content is not in the expected format.'
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
        calcinfo.retrieve_list = [
            self._OUTPUT_FILE_NAME, self._EV1_SHIFTED_FILENAME,
            self._EV2_SHIFTED_FILENAME
        ]

        codeinfo = CodeInfo()
        codeinfo.cmdline_params = [
            'align', '--input-files', ev1_filename, ev2_filename,
            '--output-files', self._EV1_SHIFTED_FILENAME,
            self._EV2_SHIFTED_FILENAME
        ]
        codeinfo.stdout_name = self._OUTPUT_FILE_NAME
        codeinfo.code_uuid = code.uuid
        calcinfo.codes_info = [codeinfo]

        return calcinfo
