"""
Rips data types
"""

from voluptuous import Schema, Optional
from aiida.orm.data.parameter import ParameterData

cmdline_parameters = {
    Optional('output-file', default='out.barcode'): str,
    'max-edge-length': float,
    Optional('cpx-dimension', default=3): int,
    Optional('field-charac'): int,
    Optional('min-persistence', default=0): float,
}


class RipsDistanceMatrixParameters(ParameterData):
    """
    Input parameters for rips_distance_matrix_persistence calculation.
    """
    schema = Schema(cmdline_parameters)

    # pylint: disable=redefined-builtin, too-many-function-args
    def __init__(self, dict=None, **kwargs):
        """
        Constructor for the data class

        Usage: ``RipsDistanceMatrixParameters(dict={'cssr': True})``

        .. note:: As of 2017-09, the constructor must also support a single dbnode
          argument (to reconstruct the object from a database node).
          For this reason, positional arguments are not allowed.
        """
        if 'dbnode' in kwargs:
            super(RipsDistanceMatrixParameters, self).__init__(**kwargs)
        else:
            # set dictionary of ParameterData
            dict = self.validate(dict)
            super(RipsDistanceMatrixParameters, self).__init__(
                dict=dict, **kwargs)

    def validate(self, parameters_dict):
        """validate parameters"""
        return RipsDistanceMatrixParameters.schema(parameters_dict)

    def cmdline_params(self,
                       distance_matrix_file_name='distance.matrix',
                       remote_folder_path=None):
        """Synthesize command line parameters

        e.g. [ ['--output-file', 'out.barcode'], ['distance_matrix.file']]

        :param distance_matrix_file_name: Name of distance matrix file
        :param remote_folder_path: Path to remote folder containing distance matrix file

        """
        parameters = []

        pm_dict = self.get_dict()
        for k, v in pm_dict.iteritems():
            parameters += ['--' + k, v]

        # distance matrix can be provided via remote folder
        if remote_folder_path is None:
            parameters += [distance_matrix_file_name]
        else:
            parameters += [remote_folder_path + distance_matrix_file_name]

        return map(str, parameters)

    @property
    def output_files(self):
        """Return list of output files to be retrieved"""
        return [self.get_dict()['output-file']]

    @property
    def output_links(self):
        """Return list of output link names"""
        return ['rips_complex']
