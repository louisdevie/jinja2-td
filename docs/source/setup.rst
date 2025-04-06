Setup
=====

Installation
------------

You can install it with pip :

.. code-block:: shell

   pip install Jinja2-TD==3.x.x

The Jinja2-TD version must match your Jinja2 version :

+----------------+-------------------------------------+
| Jinja2 version | Latest compatible Jinja2-TD version |
+================+=====================================+
| 3.1.5 - 3.1.6  | 3.1.6                               |
+----------------+-------------------------------------+
| 3.1.5 - 3.1.6  | 3.1.post2                           |
+----------------+-------------------------------------+


Import and setup
----------------

Then, import it in Python :

.. code-block:: python
   
   import jinja2td

And add the ``Introspection`` extension to a Jinja environment :

.. code-block:: python

   env = jinja2.Environment(
      extensions=[Introspection, ...],
      ...
   )

You can now start using it !