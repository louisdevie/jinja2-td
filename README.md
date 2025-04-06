# Jinja2-TD 
[![Read The Docs](https://readthedocs.org/projects/jinja2-td/badge/?version=latest)](https://jinja2-td.readthedocs.io)
[![Tests](https://github.com/louisdevie/jinja2-td/actions/workflows/tests.yml/badge.svg)](https://github.com/louisdevie/jinja2-td/actions/workflows/tests.yml)
[![PyPI](https://img.shields.io/pypi/v/jinja2-td)](https://pypi.org/project/Jinja2-TD)

Provides information about Jinja2 template dependencies.

## Install

```sh
pip install jinja2-td=3.x.x
```
[About version requirements](https://jinja2-td.readthedocs.io/en/latest/setup.html#installation)

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

[Go read the docs !](https://jinja2-td.readthedocs.io)
