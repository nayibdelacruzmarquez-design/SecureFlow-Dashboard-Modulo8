"""Configuración de Sphinx para la documentación de SecureFlow Dashboard."""

import os
import sys

sys.path.insert(0, os.path.abspath("../src"))

project = "SecureFlow Dashboard"
copyright = "2026, Nayib de la Cruz Márquez"
author = "Nayib de la Cruz Márquez"
release = "1.0.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "alabaster"
html_static_path = ["_static"]