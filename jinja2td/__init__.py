"""Provides information about Jinja2 template dependencies.

This package will plug itself into the template compiler, and provide an
interface that lets you use it without having to modify any of your existing
code.
"""

import jinja2

__ALLOWED_JINJA_VERSIONS = ("3.1.5", "3.1.6")
if jinja2.__version__ not in __ALLOWED_JINJA_VERSIONS:
    import warnings

    warnings.warn(
        f"Jinja version doesn't match: expected one of {__ALLOWED_JINJA_VERSIONS}, got {jinja2.__version__!r}",
        RuntimeWarning,
    )

from . import overrides as _
from .introspection import Introspection
from .dependencies import DependencyGraph, Template, Dependency, Target
