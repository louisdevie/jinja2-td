"""Provides information about Jinja2 template dependecies.

The way it's done is quite intrusive, but the idea is that this package does all
the dirty work so you don't have to. It provides an interface that lets you use
it without having to modifiy existing Jinja code.

BE AWARE THAT BY IMPORTING THE PACKAGE `jinja2td` OR ONE OF ITS MODULES, YOU
ALTER THE WAY JINJA WORKS, AND THAT EXISTING JINJA CODE MAY BREAK OR GET SLOWER.
"""

import jinja2

if jinja2.__version__ != "3.1.2":
    raise ImportError(
        f"Jinja version doesn't match (expected 3.1.2, got {jinja2.__version__})."
    )

from . import overrides as _
from .introspection import Introspection
from .dependencies import DependencyGraph, Template, Dependency, Target
