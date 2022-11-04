Basic usage
===========

Once you've successfully setup ``jinja2td``, you can :

Get information about a template
--------------------------------

If a template has been loaded in the environment (e.g. with ``get_template``),
you can use the ``dependencies`` attribute of the environment retrieve the static
dependencies of that template:

.. code-block:: python

   ...

   my_template = env.get_template("my_template.j2")

   ...

   # use the same template name
   template_info = env.dependencies.get_template("my_template.j2")

   # get the parent
   parent = template_info.get_parent()
   if parent is not None:
       print("This template extends", parent.target.name)
   else:
       print("This template doesn't extend another")

   # find wich templates {% include %} this one
   print("This template is included in:")
   for t in template_info.find_included():
       print(t.name)

   ...

.. note::
   Dynamic dependencies (e.g. ``{% extends variable %}``) are detected, but will
   be ignored by functions like ``get_parent`` and ``find_included``. See the
   :ref:`api_ref` for more information about dynamic dependency handling.


Find the templates actually used
--------------------------------

You can detect all the templated used during render with the ``watch`` and
``used_last_watch`` functions:

.. code-block:: python

   ...

   my_template = env.get_template("my_template.j2")

   # call before each render you want to watch 
   env.dependencies.watch()

   result = my_template.render(...)

   templates_used = env.depedencies.used_last_watch()
   print("Templates used to render my_template.j2:")
   for t in templates_used:
       print(t.name, t.file)

   ...
