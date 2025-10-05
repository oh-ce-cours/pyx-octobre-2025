# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from typing import List

sys.path.insert(0, os.path.abspath("../../.."))

# -- Project information -----------------------------------------------------

project = "Demo API"
copyright = "2025, Demo API Team"
author = "Demo API Team"
release = "1.0.0"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "myst_parser",
    "sphinx.ext.autosectionlabel",
]

# Add any paths that contain templates here, relative to this directory.
templates_path: List[str] = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns: List[str] = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "furo"

# -- Options for HTML output -------------------------------------------------

# Configuration pour GitHub Pages
html_baseurl = "https://oh-ce-cours.github.io/pyx-octobre-2025/sphinx/"

# Configuration des chemins pour GitHub Pages
html_use_opensearch = "https://oh-ce-cours.github.io/pyx-octobre-2025/sphinx/"
html_short_title = "Demo API Docs"

# Force l'utilisation de chemins absolus pour tous les assets
html_use_index = True
html_permalinks = True
html_permalinks_icon = "§"


# Configuration pour renommer _static en static pour GitHub Pages
# GitHub Pages peut avoir des problèmes avec les dossiers commençant par _
html_static_path: List[str] = ["_static"]
html_extra_path: List[str] = []

# Configuration cruciale pour GitHub Pages - force les chemins absolus
html_show_sourcelink = False
html_show_sphinx = False

# Configuration spécifique pour GitHub Pages - CRUCIAL pour les CSS
# Force l'utilisation de chemins absolus pour tous les assets statiques
html_css_files: List[str] = []
html_js_files: List[str] = []

# Configuration alternative pour GitHub Pages - Force les chemins absolus
# Cette configuration est cruciale pour que les CSS se chargent correctement
html_context = {
    "display_github": False,
    "github_user": "oh-ce-cours",
    "github_repo": "pyx-octobre-2025",
    "github_version": "main",
    "conf_py_path": "/tape_en_cours/demo_api/docs/sphinx/source/",
}

# -- Options for Furo theme ------------------------------------------------
html_title = "Demo API - Documentation"
html_logo = None  # Ajoutez ici le chemin vers votre logo si vous en avez un

# Configuration du thème Furo
html_theme_options = {
    "sidebar_hide_name": False,
    "body_max_width": None,  # Pas de limite de largeur
    "navigation_with_keys": True,
    "announcement": "🚀 Bienvenue dans la documentation Demo API ! Documentation moderne avec Sphinx et Furo.",
    "top_of_page_button": "edit",
    "source_repository": None,  # À configurer si vous avez un repo GitHub
    "source_branch": None,
    "source_directory": None,
    "footer_icons": None,  # À configurer si vous ajoutez des liens GitHub/autres
}

# Profondeur de titre pour la TdM de gauche et droite (Furo)
toc_object_entries_show = False
html_sidebars = {
    "**": [
        "sidebar/scroll-start.html",
        "sidebar/brand.html",
        "sidebar/search.html",
        "sidebar/navigation.html",
        "sidebar/ethical-ads.html",
        "sidebar/scroll-end.html",
    ]
}

# -- Configuration pour GitHub Pages (assets statiques) ---------------------


# -- Extension configuration -------------------------------------------------

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# Autodoc settings
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

# Autosummary settings
autosummary_generate = True
autosummary_generate_overwrite = True
autosummary_imported_members = True

# Type hints
typehints_fully_qualified = False
always_document_param_types = True
typehints_document_rtype = True

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "requests": ("https://requests.readthedocs.io/en/latest/", None),
    "typer": ("https://typer.tiangolo.com/", None),
}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True
