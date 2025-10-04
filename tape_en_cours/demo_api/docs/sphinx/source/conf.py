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
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "furo"

# -- Options for HTML output -------------------------------------------------

# Configuration pour GitHub Pages
html_baseurl = "https://oh-ce-cours.github.io/pyx-octobre-2025/docs-deploy/"

# Configuration des chemins pour GitHub Pages
html_use_opensearch = "https://oh-ce-cours.github.io/pyx-octobre-2025/docs-deploy/"
html_short_title = "Demo API Docs"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Configuration cruciale pour GitHub Pages - force les chemins absolus
html_show_sourcelink = False
html_show_sphinx = False

# Configuration spécifique pour GitHub Pages - CRUCIAL pour les CSS
# Force l'utilisation de chemins absolus pour tous les assets statiques
html_css_files = []
html_js_files = []

# Configuration pour forcer les chemins absolus des assets statiques
# Cette option indique à Sphinx d'utiliser des chemins absolus basés sur html_baseurl
html_use_index = True
html_add_permalinks = True
html_permalinks = True
html_permalinks_icon = "§"

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

# Configuration cruciale pour forcer les chemins absolus des assets statiques
# Cette configuration force Sphinx à utiliser des chemins absolus basés sur html_baseurl
# pour tous les assets statiques (CSS, JS, images, etc.)


# Force l'utilisation de chemins absolus pour les assets statiques
def setup(app):
    """Configuration personnalisée pour forcer les chemins absolus."""
    from sphinx.builders.html import StandaloneHTMLBuilder
    from sphinx.util import logging
    import re

    def fix_html_output(app, pagename, templatename, context, doctree):
        """Corrige les chemins des assets statiques dans le HTML généré."""
        if app.builder.name == "html":
            base_url = app.config.html_baseurl.rstrip("/")

            # Force l'utilisation de chemins absolus pour les assets statiques
            context["pathto"] = (
                lambda other, *args, **kwargs: f"{base_url}/{other.lstrip('/')}"
            )

            # Ajoute des variables de contexte pour les chemins absolus
            context["static_url"] = f"{base_url}/_static"
            context["base_url"] = base_url

    def fix_css_js_paths(app, pagename, templatename, context, doctree):
        """Corrige spécifiquement les chemins CSS et JS."""
        if app.builder.name == "html":
            base_url = app.config.html_baseurl.rstrip("/")

            # Liste des fichiers CSS et JS à corriger
            css_files = context.get("css_files", [])
            js_files = context.get("js_files", [])

            # Corrige les chemins CSS
            for i, css_file in enumerate(css_files):
                if isinstance(css_file, str) and css_file.startswith("_static/"):
                    css_files[i] = f"{base_url}/{css_file}"
                elif isinstance(css_file, (list, tuple)) and len(css_file) > 0:
                    if css_file[0].startswith("_static/"):
                        css_files[i] = (f"{base_url}/{css_file[0]}",) + css_file[1:]

            # Corrige les chemins JS
            for i, js_file in enumerate(js_files):
                if isinstance(js_file, str) and js_file.startswith("_static/"):
                    js_files[i] = f"{base_url}/{js_file}"
                elif isinstance(js_file, (list, tuple)) and len(js_file) > 0:
                    if js_file[0].startswith("_static/"):
                        js_files[i] = (f"{base_url}/{js_file[0]}",) + js_file[1:]

    app.connect("html-page-context", fix_html_output)
    app.connect("html-page-context", fix_css_js_paths)


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
