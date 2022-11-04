Setup
=====

Installation
------------

You can install it with pip :

.. code-block:: shell

   pip install Jinja2-TD==3.x.x

The Jinja2-TD version must match your Jinja2 version. Currently, only the latest version (3.1.2) is supported.


Import and setup
----------------

Then, import it in Python:

.. code-block:: python
   
   import jinja2td

And add the ``Introspection`` extension to a Jinja environment:

.. code-block:: python

   env = jinja2.Environment(
      extensions=[Introspection, ...],
      ...
   )

You can now start using it!
