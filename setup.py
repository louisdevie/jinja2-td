from setuptools import setup

with open("README.md", "rt", encoding="utf8") as f:
    README = f.read()

setup(
    name="Jinja2-TD",
    version="3.1.6",
    description="Jinja2 template dependency insight",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Louis DEVIE",
    url="https://github.com/louisdevie/jinja2-td",
    packages=["jinja2td"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.8",
    ],
    keywords=[
        "jinja",
        "jinja2",
        "template",
        "dependency",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Jinja2 >=3.1.5, <=3.1.6",
    ],
)
