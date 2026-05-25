import os, sys
sys.path.insert(0, os.path.abspath('../..'))
project = "Netflix EDA Reproduction"
copyright = "2026"
author = "Your Group"
extensions = ["sphinx.ext.autodoc","sphinx.ext.napoleon","sphinx.ext.viewcode"]
html_theme = "sphinx_rtd_theme"
napoleon_google_docstring = True
