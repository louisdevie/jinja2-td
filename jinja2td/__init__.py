"""Provides information about Jinja2 template dependecies.

The way it's done is quite intrusive, but the idea is that this package does all
the dirty work so you don't have to. It provides an interface that lets you use
it without having to modifiy existing Jinja code.

BE AWARE THAT BY IMPORTING THE PACKAGE `jinja2td` OR ONE OF ITS MODULES, YOU
ALTER THE WAY JINJA WORKS, AND THAT EXISTING JINJA CODE MAY BREAK OR GET SLOWER.
"""

import jinja2

__ALLOWED_JINJA_VERSIONS = ("3.1.2", "3.1.3", "3.1.4")
if jinja2.__version__ not in __ALLOWED_JINJA_VERSIONS:
    import warnings

    warnings.warn(
        f"Jinja version doesn't match: expected one of {__ALLOWED_JINJA_VERSIONS}, got {jinja2.__version__!r}",
        RuntimeWarning,
    )

from . import overrides as _
from .introspection import Introspection
from .dependencies import DependencyGraph, Template, Dependency, Target
