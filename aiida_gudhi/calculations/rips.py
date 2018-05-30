"""
Calculations provided by plugin

Register calculations via the "aiida.calculations" entry point in setup.json.
"""

from aiida.orm.calculation.job import JobCalculation
from aiida.common.utils import classproperty
from aiida.common.exceptions import (InputValidationError, ValidationError)
from aiida.common.datastructures import (CalcInfo, CodeInfo)
from aiida.orm import DataFactory

ParameterData = DataFactory('parameter')
SinglefileData = DataFactory('singlefile')
RemoteData = DataFactory('remote')
RipsDistanceMatrixParameters = DataFactory('gudhi.rdm')


class RipsDistanceMatrixCalculation(JobCalculation):
    """
    Calculating persistence homology diagram from distance matrix.
    """

    _REMOTE_FOLDER_LINK = 'remote_folder/'

    def _init_internal_params(self):
        """
        Init internal parameters at class load time
        """
        # reuse base class function
        super(RipsDistanceMatrixCalculation, self)._init_internal_params()

        self._default_parser = 'gudhi.rdm'

    @classproperty
    def _use_methods(cls):
        """
        Add use_* methods for calculations.

        Code below enables the usage
        my_calculation.use_parameters(my_parameters)
        """
        use_dict = JobCalculation._use_methods
        use_dict.update({
            "parameters": {
                'valid_types': RipsDistanceMatrixParameters,
                'additional_parameter': None,
                'linkname': 'parameters',
                'docstring': 'add command line parameters',
            },
            "distance_matrix": {
                'valid_types': SinglefileData,
                'additional_parameter': None,
                'linkname': 'distance_matrix',
                'docstring': "distance matrix of point cloud",
            },
            "remote_folder": {
                'valid_types': RemoteData,
                'additional_parameter': None,
                'linkname': 'remote_folder',
                'docstring': "remote folder containing distance matrix",
            },
        })
        return use_dict

    def _validate_inputs(self, inputdict):
        """ Validate input links.
        """
        # Check inputdict
        try:
            parameters = inputdict.pop(self.get_linkname('parameters'))
        except KeyError:
            raise InputValidationError("No parameters specified for this "
                                       "calculation")
        if not isinstance(parameters, RipsDistanceMatrixParameters):
            raise InputValidationError("parameters not of type "
                                       "RipsDistanceMatrixParameters")
        # Check code
        try:
            code = inputdict.pop(self.get_linkname('code'))
        except KeyError:
            raise InputValidationError("No code specified for this "
                                       "calculation")

        # Check input files
        try:
            distance_matrix = inputdict.pop(
                self.get_linkname('distance_matrix'))
            if not isinstance(distance_matrix, SinglefileData):
                raise InputValidationError(
                    "distance_matrix not of type SinglefileData")
            symlink = None

        except KeyError:
            distance_matrix = None

            try:
                remote_folder = inputdict.pop(
                    self.get_linkname('remote_folder'))
                if not isinstance(remote_folder, RemoteData):
                    raise InputValidationError(
                        "remote_folder is not of type RemoteData")

                comp_uuid = remote_folder.get_computer().uuid
                remote_path = remote_folder.get_remote_path()
                symlink = (comp_uuid, remote_path, self._REMOTE_FOLDER_LINK)

            except KeyError:
                raise InputValidationError(
                    "Need to provide either distance_matrix or remote_folder")

        # Check that nothing is left unparsed
        if inputdict:
            raise ValidationError("Unrecognized inputs: {}".format(inputdict))

        return parameters, code, distance_matrix, symlink

    def _prepare_for_submission(self, tempfolder, inputdict):
        """
        Create input files.

            :param tempfolder: aiida.common.folders.Folder subclass where
                the plugin should put all its files.
            :param inputdict: dictionary of the input nodes as they would
                be returned by get_inputs_dict
        """
        parameters, code, distance_matrix, symlink = \
                self._validate_inputs(inputdict)

        # Prepare CalcInfo to be returned to aiida
        calcinfo = CalcInfo()
        calcinfo.uuid = self.uuid
        calcinfo.remote_copy_list = []
        calcinfo.retrieve_list = parameters.output_files

        codeinfo = CodeInfo()
        codeinfo.code_uuid = code.uuid

        if distance_matrix is not None:
            calcinfo.local_copy_list = [
                [
                    distance_matrix.get_file_abs_path(),
                    distance_matrix.filename
                ],
            ]
            codeinfo.cmdline_params = parameters.cmdline_params(
                distance_matrix_file_name=distance_matrix.filename)
        else:
            calcinfo.remote_symlink_list = [symlink]
            codeinfo.cmdline_params = parameters.cmdline_params(
                remote_folder_path=self._REMOTE_FOLDER_LINK)

        calcinfo.codes_info = [codeinfo]

        return calcinfo
