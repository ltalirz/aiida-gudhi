# -*- coding: utf-8 -*-
"""Submit a test calculation on localhost.

Usage: verdi run submit.py

Note: This script assumes you have set up computer and code as in README.md.
"""
import aiida_gudhi.tests as gt
import os


class TestRips():
    def setUp(self):
        try:
            self.computer = Computer.get('localhost')
        except NotExistent:
            self.computer = gt.get_localhost_computer().store()

        self.code = gt.get_code(
            plugin='gudhi.rdm', computer=self.computer).store()

    def test_submit_rips(self):
        """Test submitting a calculation"""
        code = self.code

        # set up calculation
        calc = code.new_calc()
        calc.label = "compute rips from distance matrix"
        calc.set_max_wallclock_seconds(1 * 60)
        calc.set_withmpi(False)
        calc.set_resources({"num_machines": 1, "num_mpiprocs_per_machine": 1})

        # Prepare input parameters
        from aiida.orm import DataFactory
        Parameters = DataFactory('gudhi.rdm')
        parameters = Parameters(dict={'max-edge-length': 4.2})
        calc.use_parameters(parameters)

        SinglefileData = DataFactory('singlefile')
        distance_matrix = SinglefileData(
            file=os.path.join(gt.TEST_DIR, 'sample_distance.matrix'))
        calc.use_distance_matrix(distance_matrix)

        calc.store_all()
        calc.submit()
        #calc.submit_test(folder=gt.get_temp_folder())


t = TestRips()

t.setUp()
t.test_submit_rips()
