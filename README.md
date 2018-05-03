# M2L

Module-to-library generate a Python package from a module (or set of modules).
The idea is to free the user from the (possibly) cumbersome process of creating
the *setup* schema for simple Python packages.

M2L provides a command-line interface to get the necessary information from
the user like the module(s) to consider and package name.

# How to use

To setup a package from a single Python module `myapp.py`,
```bash
# m2l init myapp.py --pkgname=xapp --pkgimp=myapp
```

