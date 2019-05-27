"""Policy compliance

This checks that recipes are in accordance with policy (as far as it
can be mechanically checked).

"""

import glob
import os

from . import LintCheck, ERROR, WARNING, INFO


class uses_vcs_url(LintCheck):
    """The recipe downloads source from a VCS

    Please build from source archives and don't use the ``git_url``,
    ``svn_url`` or ``hg_url`` feature of conda.

    """
    def check_source(self, source, section):
        for vcs in ('git', 'svn', 'hg'):
            if f"{vcs}_url" in source:
                self.message(section=f"{section}/{vcs}_url")

class folder_and_package_name_must_match(LintCheck):
    """The recipe folder and package name do not match.

    For clarity, the name of the folder the ``meta.yaml`` resides,
    in and the name of the toplevel package should match.
    """
    def check_recipe(self, recipe):
        recipe_base_folder, _, _ = recipe.reldir.partition('/')
        if recipe.name !=  recipe_base_folder:
            self.message(section='package/name')


class gpl_requires_license_distributed(LintCheck):
    """The recipe packages GPL software but is missing copy of license.

    The GPL requires that a copy of the license accompany all distributions
    of the software. Please add::

        about:
            license_file: name_of_license_file

    If the upstream tar ball does not include a copy, please ask the
    authors of the software to add it to their distribution archive.
    """
    severity = WARNING
    requires = ["missing_license"]

    def check_recipe(self, recipe):
        if 'gpl' in recipe.get('about/license').lower():
            if not recipe.get('about/license_file', ''):
                self.message('about/license')


class should_not_use_fn(LintCheck):
    """The recipe uses source/fn

    There is no need to specify the filename as the URL should give a name
    and it will in most cases be unpacked automatically.
    """
    def check_source(self, source, section):
        if 'fn' in source:
            self.message(section=section+'/fn')


class has_windows_bat_file(LintCheck):
    """The recipe directory contains a ``bat`` file.

    Bioconda does not currently build packages for Windows (and has at
    this time no plans to change this), so these files cannot be
    tested.

    Please remove any ``*.bat`` files generated by ``conda skeleton``
    from the recipe directory.

    """
    def check_recipe(self, recipe):
        for fname in glob.glob(os.path.join(recipe.dir, '*.bat')):
            self.message(fname=fname)


class long_summary(LintCheck):
    """The summary line is rather long

    Consider using the description field for longer text::

    about:
      summary: Fancy Read Simulator (makes drinks)
      description: |
        XYZ is a very fancy read simulator that will not just make coffee
        while you are waiting but prepare all kinds of exquisite caffeeinated
        beverages from freshly roasted, single source beans ground to match
        ambient humidity.

    This will fit better into the templates listing and describing
    recipes, which assume the summary to be a title and the
    description to be one or more paragraphs.

    """
    severity = WARNING
    max_length = 120
    def check_recipe(self, recipe):
        if len(recipe.get('about/summary', '')) > self.max_length:
            self.message('about/summary')
