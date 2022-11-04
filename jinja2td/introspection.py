"""The Jinja2 extension for jinja2-td.
"""

import jinja2
from jinja2.ext import Extension

from . import overrides as _
from .dependencies import DependencyGraph


class Introspection(Extension):
    """An extension that provides access to the features of jinja2td."""

    def __init__(self, environment):
        super().__init__(environment)

        self.__deps = DependencyGraph()

        environment.extend(dependencies=self.__deps)

    def preprocess(self, source, name, filename=None):
        self.__deps._add_template(name, filename)
        return source
