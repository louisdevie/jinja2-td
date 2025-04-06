# Jinja2-TD  ![Read The Docs](https://readthedocs.org/projects/jinja2-td/badge/?version=latest)

Provides information about Jinja2 template dependencies.

## Install

```sh
pip install Jinja2-TD==3.x.x
```

## Example

```python
...

my_template = env.get_template("my_template.j2")

...

template_info = env.dependencies.get_template("my_template.j2")

parent = template_info.get_parent()
if parent is not None:
   print("This template extends", parent.target.name)
else:
   print("This template doesn't extend another")
```

[Go read the docs!](https://jinja2-td.readthedocs.io)
