# Jinja2-TD

Provides information about Jinja2 template dependencies.

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