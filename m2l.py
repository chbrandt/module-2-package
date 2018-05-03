from __future__ import print_function, absolute_import

import os

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
@click.option('--author', default='', type=str, help="Name of package author")
@pass_options
def cli(options, pkgname, pkgimp, author):
    """
    Module-to-package setup tool
    """
    options['pkgname'] = pkgname
    options['pkgimp'] = pkgimp
    options['author'] = author


class Package(object):
    def __init__(self, options):
        assert options['pymod']
        self.pymod = options['pymod']
        self.set_pkgname(options['pkgname'])
        self.set_pkgimp(options['pkgimp'])
        assert self.pkgname and self.pkgimp

        self.author = options['author']

    def set_pkgname(self, pkgname):
        if pkgname is None or pkgname.strip() == '':
            pkgname = self.pymod.strip('.py')
            #TODO: normalize better pakcage-name (whitespaces, periods, etc.)
        self.pkgname = pkgname

    def set_pkgimp(self, pkgimp):
        if pkgimp is None or pkgimp.strip() == '':
            pkgimp = self.pymod.strip('.py')
            #TODO: normalize better package import/namespace
        self.pkgimp = pkgimp


@cli.command()
@click.argument('pymod')
@pass_options
def init(options, pymod):
    """
    Initialize package schema from '.py' module
    """
    print('init:', pymod)

    options['pymod'] = pymod
    pkg = Package(options)
    do_readme(pkg)


def do_readme(pkg):
    """
    Render README file
    """
    temp = templates.get('README.md')
    readme = temp.render(package_name=pkg.pkgname, author_name=pkg.author)

    pkgdir = os.path.abspath(pkg.pkgname)
    if not (os.path.exists(pkgdir) or os.path.isdir(pkgdir)):
        os.mkdir(pkgdir)
    readme_file = os.path.join(pkgdir,'README.md')

    with open(readme_file, 'w') as fp:
        fp.write(readme)


def _license():
    pass

def _setuptools():
    pass


def _versioneer():
    pass


def _tests():
    pass


def _conda():
    pass


class templates:
    @staticmethod
    def get(name):
        from jinja2 import Environment, FileSystemLoader
        _env = Environment(loader=FileSystemLoader(THIS_DIR))
        _file = os.path.join('templates', name)
        return _env.get_template(_file)



if __name__ == "__main__":
    cli()
