# Module-2-Library

Module-to-library generate a Python package from a module (or set of modules).
The idea is to free the user from the (possibly) cumbersome process of creating
the *setup* schema for simple Python packages.

M2L provides a command-line interface to get the necessary information from
the user like the module(s) to consider and package name.


# How to use

To setup a package from a Python module, `myapp.py`, we may simply type:

```bash
# m2l myapp.py
```


`M2L` though offers a number of options to better define the output package:

```bash
# m2l --help
Usage: m2l [OPTIONS] PYMOD

  Module-to-package setup tool

Options:
  --pkgname TEXT      Name of package to install
  --pkgimp TEXT       Namespace of package to import
  --version TEXT      Version of the package
  --requires TEXT     Comma-separated list of dependencies
  --author TEXT       Name of package author
  --description TEXT  Short package description
  --dest TEXT         Top directory where package should be created
  --entrypoint TEXT   Function in module to use as entrypoint
  --datadir TEXT      Data directory (recursively copied)
  --help              Show this message and exit.
```
