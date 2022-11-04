Jinja2-TD
=========

Provides information about Jinja2 template dependencies.

The way it's done is quite intrusive, but the idea is that this package does all
the dirty work so you don't have to. It provides an interface that lets you use
it without having to modifiy existing Jinja code.

**Be aware that by importing the package** ``jinja2td`` **or one of its modules, you
alter the way jinja works, and that existing jinja code may break or get slower.**

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   setup
   usage
   api