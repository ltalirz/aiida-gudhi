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
RipsDistanceMatrixParameters = DataFactory('gudhi.rdm')


class RipsDistanceMatrixCalculation(JobCalculation):
    """
    Calculating persistence homology diagram from distance matrix.
    """

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
        except KeyError:
            raise InputValidationError(
                "No distance matrix specified for calculation")

        # Check that nothing is left unparsed
        if inputdict:
            raise ValidationError("Unrecognized inputs: {}".format(inputdict))

        return parameters, code, distance_matrix

    def _prepare_for_submission(self, tempfolder, inputdict):
        """
        Create input files.

            :param tempfolder: aiida.common.folders.Folder subclass where
                the plugin should put all its files.
            :param inputdict: dictionary of the input nodes as they would
                be returned by get_inputs_dict
        """
        parameters, code, distance_matrix = \
                self._validate_inputs(inputdict)

        # Prepare CalcInfo to be returned to aiida
        calcinfo = CalcInfo()
        calcinfo.uuid = self.uuid
        calcinfo.local_copy_list = [
            [distance_matrix.get_file_abs_path(), distance_matrix.filename],
        ]
        calcinfo.remote_copy_list = []
        calcinfo.retrieve_list = parameters.output_files

        codeinfo = CodeInfo()
        codeinfo.cmdline_params = parameters.cmdline_params(
            distance_matrix_file_name=distance_matrix.filename)
        codeinfo.code_uuid = code.uuid
        calcinfo.codes_info = [codeinfo]

        return calcinfo
