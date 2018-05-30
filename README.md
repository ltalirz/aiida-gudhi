# aiida-gudhi

AiiDA plugin for the [GUDHI](http://gudhi.gforge.inria.fr/) library for topological data analysis.

# Installation

```shell
git clone https://github.com/ltalirz/aiida-gudhi .
cd aiida-gudhi
pip install -e .  # also installs aiida, if missing (but not postgres)
#pip install -e .[precommit,testing] # install extras for more features
verdi quicksetup  # better to set up a new profile
verdi calculation plugins  # should now show your calclulation plugins
```

# Usage

Here goes a complete example of how to submit a test calculation using this plugin.

# License

MIT

# Contact

leopold.talirz@gmail.com
