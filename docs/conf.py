# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'sanporobot'
copyright = '2026, sanporobot'
author = 'sanporobot'
release = 'v4'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

templates_path = ['_templates']
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    'Lib/**',
    'Scripts/**',
    'Include/**',
    'env/**',
    'venv/**',
    '.venv/**',
    '**/site-packages/**',
]

language = 'zh_CN'
locale_dirs = ['locale/']
gettext_compact = False

myst_enable_extensions = [
    'colon_fence',
    'deflist',
    'tasklist',
]
myst_heading_anchors = 3

autosummary_generate = True
autodoc_typehints = 'description'
todo_include_todos = False

intersphinx_mapping = {
     'python': ('https://docs.python.org/3', None),
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
