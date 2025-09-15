"""Sphinx documentation configuration file."""

from datetime import datetime
import os
import pathlib
import shutil

from ansys_sphinx_theme import get_version_match

from ansys.lumerical.core import __version__
from ansys.lumerical.core.autodiscovery import __min_supported_lum_release__

# Project information
project = "ansys-lumerical-core"
copyright = f"(c) {datetime.now().year} ANSYS, Inc. All rights reserved"
author = "ANSYS, Inc."
release = version = __version__
supported_lum_release = f"20{__min_supported_lum_release__['year']} R{__min_supported_lum_release__['release']}"
cname = os.getenv("DOCUMENTATION_CNAME", "")
switcher_version = get_version_match(__version__)

# Select desired logo, theme, and declare the html title
html_theme = "ansys_sphinx_theme"
html_short_title = html_title = "PyLumerical"

# specify the location of your github repo
html_theme_options = {
    "github_url": "https://github.com/ansys/pylumerical",
    "show_prev_next": False,
    "show_breadcrumbs": True,
    "additional_breadcrumbs": [
        ("PyAnsys", "https://docs.pyansys.com/"),
    ],
    "switcher": {
        "json_url": f"https://{cname}/versions.json",
        "version_match": switcher_version,
    },
    "check_switcher": False,
    "logo": "pyansys",
}

# Sphinx extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "numpydoc",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_design",  # Needed for cards
    "sphinx.ext.extlinks",
    "nbsphinx",
]

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    # kept here as an example
    # "scipy": ("https://docs.scipy.org/doc/scipy/reference", None),
    # "numpy": ("https://numpy.org/devdocs", None),
    # "matplotlib": ("https://matplotlib.org/stable", None),
    # "pandas": ("https://pandas.pydata.org/pandas-docs/stable", None),
    # "pyvista": ("https://docs.pyvista.org/", None),
    # "grpc": ("https://grpc.github.io/grpc/python/", None),
}

# numpydoc configuration
numpydoc_show_class_members = False
numpydoc_xref_param_type = True

# Consider enabling numpydoc validation. See:
# https://numpydoc.readthedocs.io/en/latest/validation.html#
numpydoc_validate = True
numpydoc_validation_checks = {
    "GL06",  # Found unknown section
    "GL07",  # Sections are in the wrong order.
    "GL08",  # The object does not have a docstring
    "GL09",  # Deprecation warning should precede extended summary
    "GL10",  # reST directives {directives} must be followed by two colons
    "SS01",  # No summary found
    "SS02",  # Summary does not start with a capital letter
    # "SS03", # Summary does not end with a period
    "SS04",  # Summary contains heading whitespaces
    # "SS05", # Summary must start with infinitive verb, not third person
    "RT02",  # The first line of the Returns section should contain only the
    # type, unless multiple values are being returned"
}

# Strip Python prompt from code block copy, this will make copied code easier to use
copybutton_prompt_text = r">>> ?|\.\.\. ?"
copybutton_prompt_is_regexp = True

#Ignore files for build

exclude_patterns =["conf.py"]

# Skipping members
def autodoc_skip_member_custom(app, what, name, obj, skip, options):
    """Skip members that are not documented."""
    return True if obj.__doc__ is None else None  # need to return none if exclude is false otherwise it will interfere with other skip functions


# nbpsphinx configurations

nbsphinx_execute = "never"

nbsphinx_custom_formats = {".py": ["jupytext.reads", {"fmt": ""}]}

nbsphinx_prolog = """


.. grid:: 1 2 2 2

    .. grid-item::

        .. button-link:: {base_path}/{ipynb_file_path}
            :color: secondary
            :shadow:
            :align: center

            :octicon:`download` Download Jupyter Notebook (.ipynb)
            

    .. grid-item::

        .. button-link:: {base_path}/{py_file_path}
            :color: secondary
            :shadow:
            :align: center

            :octicon:`download` Download Python script (.py)
    
----
""".format(
    base_path = f"https://{cname}/version/{get_version_match(version)}",
    py_file_path ="{{ env.docname }}.py",
    ipynb_file_path ="{{ env.docname }}.ipynb"
)

# Define auxiliary functions needed for examples


def copy_examples_to_source_dir(app):
    """Copy examples to source directory for nbsphinx."""
    source_dir = pathlib.Path(app.srcdir)

    shutil.copytree(source_dir.parent.parent / "examples", source_dir / "examples", dirs_exist_ok=True)


def remove_examples_from_source_dir(app, exception):
    """Remove examples from source directory after build."""
    source_dir = pathlib.Path(app.srcdir)
    shutil.rmtree(source_dir / "examples")

def copy_examples_to_output_dir(app, exception):
    """Copy examples to output directory."""
    
    source_dir = pathlib.Path(app.srcdir)
    build_dir = pathlib.Path(app.outdir)

    shutil.copytree(source_dir.parent.parent / "examples", build_dir / "examples", dirs_exist_ok=True)

rst_prolog = ""

rst_prolog += f""".. |supported_lum_release| replace:: {supported_lum_release}"""

# static path
html_static_path = ["_static"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# Keep these while the repository is private
linkcheck_ignore = [
    "https://github.com/ansys/pylumerical/*",
    "https://pypi.org/project/ansys-lumerical-core",
]

# If we are on a release, we have to ignore the "release" URLs, since it is not
# available until the release is published.
if switcher_version != "dev":
    linkcheck_ignore.append(f"https://github.com/ansys/ansys.lumerical.core/releases/tag/v{__version__}")


# Define extlinks

extlinks = {"examples_url": (f"{html_theme_options['github_url']}/blob/main/examples/%s", "%s")}


# Define setup function


def setup(app):
    """Sphinx setup function."""
    app.connect("builder-inited", copy_examples_to_source_dir)
    app.connect("autodoc-skip-member", autodoc_skip_member_custom)
    app.connect("build-finished", remove_examples_from_source_dir)
    app.connect("build-finished", copy_examples_to_output_dir)
    
    
