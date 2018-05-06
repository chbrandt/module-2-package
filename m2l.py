from __future__ import print_function, absolute_import

import os
import shutil

import click
echo = click.echo

# This file's directory
THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class Options(dict):
    def __init__(self):
        super(Options,self).__init__()
        self['pkgname'] = None
        self['pkgimp'] = None
        self['pymod'] = ''
        self['author'] = ''


pass_options = click.make_pass_decorator(Options, ensure=True)

@click.group()
@click.option('--pkgname', default=None, type=str, help="Name of package to install")
@click.option('--pkgimp', default=None, type=str, help="Namespace of package to import")
@click.option('--author', default=None, type=str, help="Name of package author")
@click.option('--description', default=None, type=str, help="Short package description")
@pass_options
def cli(options, pkgname, pkgimp, author, description):
    """
    Module-to-package setup tool
    """
    options['pkgname'] = pkgname
    options['pkgimp'] = pkgimp
    options['author'] = author
    options['description'] = description


class Package(object):
    """
    Handles package metadata; then used by (jinja) templates

    Attributes:
     - pymod
     - pkgname
     - pkgimp
     - version
     - description
     - author
    """
    version = 0.1

    def __init__(self, options):
        assert options['pymod']
        self.pymod = options['pymod']

        self.pkgimp = self.set_pkgimp(options['pkgimp'])
        self.pkgname = self.set_pkgname(options['pkgname'])
        assert self.pkgname and self.pkgimp

        self.author = self.set_author(options['author'])
        self.description = self.set_description(options['description'])
        assert not(self.author is None or self.description is None)

    def set_pkgname(self, pkgname):
        if pkgname is None or pkgname.strip() == '':
            #TODO: normalize better pakcage-name (whitespaces, periods, etc.)
            pkgname = self.pymod.rstrip('\.py')
        return pkgname

    def set_pkgimp(self, pkgimp):
        if pkgimp is None or pkgimp.strip() == '':
            #TODO: normalize better package import/namespace
            pkgimp = self.pymod.rstrip('\.py')
        return pkgimp

    def set_author(self, author):
        return author or "Anonymous author"

    def set_description(self, description):
        return description or "The {} package.".format(self.pkgname)

    @property
    def path(self):
        return os.path.abspath(self.pkgname)


@cli.command()
@click.argument('pymod')
@pass_options
def init(options, pymod):
    """
    Initialize package schema from '.py' module
    """
    assert os.path.exists(pymod), "Module '{}' not found.".format(pymod)

    options['pymod'] = pymod
    pkg = Package(options)
    do_package(pkg)
    # do_git(pkg)
    do_readme(pkg)
    do_setuptools(pkg)
    # do_versioneer(pkg)
    do_tests(pkg)
    do_conda(pkg)


def do_package(pkg):
    """
    Copy module to package
    """
    path_pkg = pkg.path
    if os.path.exists(path_pkg) and os.path.isdir(path_pkg):
        shutil.rmtree(path_pkg)
    os.mkdir(path_pkg)
    path_src = os.path.join(path_pkg, pkg.pkgimp)
    os.mkdir(path_src)
    shutil.copy(pkg.pymod, path_src)
    templates.render('__init__.py', pkg, subdir=pkg.pkgimp)


def do_readme(pkg):
    """
    Render README file
    """
    templates.render('README.md', pkg)


def do_setuptools(pkg):
    """
    Render setup.{py,cfg} files
    """
    for fname in ['setup.cfg','setup.py']:
        templates.render(fname, pkg)


def do_git(pkg):
    """
    Create git repository, necessary to versioneer
    """
    pass


def do_versioneer(pkg):
    """
    Setup versioneer to package
    """
    _path = pkg.path
    assert os.path.exists(_path) and os.path.isdir(_path),\
            "Was expecting to find '{}' path. This is a bug.".format(_path)
    _pwd = os.getcwd()
    try:
        os.chdir(_path)
        os.system('versioneer install')
    finally:
        os.chdir(_pwd)


def do_tests(pkg):
    """
    Copy tests structure
    """
    from distutils.dir_util import copy_tree
    copy_tree(os.path.join(templates.path, 'tests'), os.path.join(pkg.path, 'tests'))
    shutil.copy(os.path.join(templates.path, 'test.py'), pkg.path)


def do_conda(pkg):
    """
    Render conda-recipe
    """
    templates.render('meta.yaml', pkg, subdir='conda_recipe')


def _license():
    pass


class templates:
    path = os.path.join(THIS_DIR, 'templates')

    @classmethod
    def get(cls, name):
        from jinja2 import Environment, FileSystemLoader
        _env = Environment(loader=FileSystemLoader(cls.path),
                           keep_trailing_newline=True)
        return _env.get_template(name)

    @staticmethod
    def render(name, pkg, subdir=None):
        def assure_dir(path):
            if not (os.path.exists(path) or os.path.isdir(path)):
                os.mkdir(path)

        temp = templates.get(name)
        cont = temp.render(pkg=pkg)

        write_to = pkg.path
        assure_dir(write_to)
        if subdir:
            write_to = os.path.join(write_to, subdir)
            assure_dir(write_to)
        write_to = os.path.join(write_to, name)

        with open(write_to, 'w') as fp:
            fp.write(cont)


if __name__ == "__main__":
    cli()
