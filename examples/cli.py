#!/usr/bin/env runaiida
# -*- coding: utf-8 -*-
import os
import click


@click.command('cli')
@click.argument('codelabel')
@click.option('--submit', is_flag=True, help='Actually submit calculation')
def main(codelabel, submit):
    """Command line interface for testing and submitting calculations.

    This script extends submit.py, adding flexibility in the selected code/computer.

    Run './cli.py --help' to see options.
    """
    code = Code.get_from_string(codelabel)

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

    if submit:
        calc.store_all()
        calc.submit()
        print("submitted calculation; calc=Calculation(uuid='{}') # ID={}"\
                .format(calc.uuid,calc.dbnode.pk))
    else:
        subfolder, script_filename = calc.submit_test()
        path = os.path.relpath(subfolder.abspath)
        print("submission test successful")
        print("Find remote folder in {}".format(path))
        print("In order to actually submit, add '--submit'")


if __name__ == '__main__':
    main()
