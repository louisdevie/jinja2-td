"""Classes to represent template dependencies.
"""
import jinja2
from typing import Optional, List, Dict


class Target:
    """The target of a dependency.

    A target is dynamic if it is not hard-coded in the template, in wich case
    the name of the target is unknown until it is resolved.
    """

    def __init__(self, dynamic: bool, name: Optional[str]):
        """Initialises a new `Target` class.

        This class should not be instanciated manually.
        """
        self.__dynamic = dynamic
        self.__name = name

    def __repr__(self):
        return f"Target(dynamic={self.__dynamic}, name={self.__name})"

    def __eq__(self, other):
        if not isinstance(other, Target):
            return NotImplemented

        return self.__dynamic == other.__dynamic and self.__name == other.__name

    @property
    def is_dynamic(self) -> bool:
        """True if the target name can't be known until the template is
        rendered.
        """
        return self.__dynamic

    @property
    def name(self) -> Optional[str]:
        """The name of the target template, or `None` if the target is dynamic."""
        return self.__name


class _ResolvedTarget:
    def __init__(self, name: str):
        self.__name = name
        self.__last_watch = True

    @property
    def last_watch(self) -> bool:
        return self.__last_watch

    def watch_reset(self):
        self.__last_watch = False

    @property
    def name(self) -> str:
        return self.__name


class Dependency:
    """A dependency to one or more templates."""

    def __init__(
        self,
        dependency_type: str,
        targets: List[Target],
        with_context: Optional[bool] = None,
        ignore_missing: Optional[bool] = None,
        imported_as: Optional[str] = None,
        imported_names: Optional[List[str]] = None,
    ):
        """Initialises a new `Dependency` class.

        This class should not be instanciated manually.
        """
        self.__type = dependency_type
        self.__targets = targets
        self.__with_context = with_context
        self.__ignore_missing = ignore_missing
        self.__imported_as = imported_as
        self.__imported_names = imported_names
        self.__resolved: List[_ResolvedTarget] = []

    def _resolve(self, name: str):
        self.__resolved.append(_ResolvedTarget(name))

    def _watch_reset(self):
        for r in self.__resolved:
            r._reset()

    @property
    def type(self) -> str:
        """The type of dependency. May be one of ``"extends"``, ``"include"`` or
        ``"import"``.
        """
        return self.__type

    @property
    def target(self) -> Optional[Target]:
        """The target of the dependency, if there is only one, or ``None``.

        .. note::
           Use `targets <#jinja2td.Dependency.targets>`_ instead if you
           need to handle multiple targets.
        """
        return self.__targets[0] if len(self.__targets) == 1 else None

    @property
    def targets(self) -> List[Target]:
        """All the targets of the dependency, in order.

        For example, an ``{% include ['template', 'fallback'] %}`` will have two
        targets.
        """
        return self.__targets.copy()

    @property
    def with_context(self) -> Optional[bool]:
        """Wether the context is passed to the dependency or not.

        .. note::
           Only available with ``"include"`` and ``"import"`` dependecies.
        """
        return self.__with_context

    @property
    def ignore_missing(self) -> Optional[bool]:
        """Wether the dependency is optional or not.

        .. note::
           Only available with ``"include"`` dependecies.
        """
        return self.__ignore_missing

    @property
    def imported_as(self) -> Optional[str]:
        """Wether the dependency is optional or not.

        .. note::
           Only available with ``"import"`` dependecies.
        """
        return self.__imported_as

    @property
    def imported_names(self) -> Optional[List[str]]:
        """Wether the dependency is optional or not.

        .. note::
           Only available with ``"import"`` dependecies.
        """
        return self.__imported_names

    @property
    def resolved(self) -> List[str]:
        """The names of the templates actually imported by this dependency.

        .. warning::
           Templates used by async environments aren't taken into account by
           default. See `DependencyGraph.used_last_watch <#jinja2td.DependencyGraph.used_last_watch>`_
           for more information.
        """
        return [r.name for r in self.__resolved]

    @property
    def resolved_last_watch(self) -> List[str]:
        """The names of the templates imported during the last watch.="""
        return [r.name for r in self.__resolved if r.last_watch]


class Template:
    """Represent a template in the dependency graph.

    This is NOT a Jinja2 template.
    """

    def __init__(self, name: str, file: Optional[str], graph: "DependencyGraph"):
        """Initialises a new `Template` class.

        This class should not be instanciated manually.
        """
        self.__name = name
        self.__file = file
        self.__deps: List[Dependency] = []
        self.__modified = False
        self.__graph = graph

    def _set_modified(self):
        self.__modified = False

    def _add_dependency(self, dependency: Dependency) -> int:
        for i, d in enumerate(self.__deps):
            if d == dependency:
                return i  # don't register the same dependency twice
        self.__deps.append(dependency)
        return len(self.__deps) - 1

    def _resolve_dependency(self, dependency_id: int, name: str):
        self.__deps[dependency_id]._resolve(name)

    def _watch_reset(self):
        for d in self.__deps:
            d._watch_reset()

    @property
    def name(self) -> str:
        """The name of the template."""
        return self.__name

    @property
    def file(self) -> Optional[str]:
        """The source file of the template, or ``None`` if the template wasn't
        loaded from a file.
        """
        return self.__file

    @property
    def dependencies(self) -> List[Dependency]:
        """The dependencies of this template."""
        return self.__deps.copy()

    @property
    def was_modified(self) -> bool:
        """`True` if the template was loaded multiple times."""
        return self.__modified

    def get_includes(self) -> List[Dependency]:
        """Get all ``"include"`` dependencies.

        :returns: The list of al ``"include"`` dependencies.
        """
        return [d for d in self.__deps if d.type == "include"]

    def get_imports(self) -> List[Dependency]:
        """Get all ``"import"`` dependencies.

        :returns: The list of all ``"import"`` dependencies.
        """
        return [d for d in self.__deps if d.type == "import"]

    def get_parent(self) -> Optional[Dependency]:
        """Get the parent template, if there is one.

        :returns: An ``"extends"`` dependency or ``None``.
        """
        extends = [d for d in self.__deps if d.type == "extends"]
        if len(extends) == 1:
            return extends[0]
        else:
            return None

    def find_included(self) -> List["Template"]:
        """Get the templates that include this one.

        :returns: The list of templates with an ``"include"`` dependency
                  targeting this template.
        """
        found = []

        for t in self.__graph.templates:
            for d in t.get_includes():
                if Target(False, self.name) in d.targets:
                    found.append(t)

        return found

    def find_imported(self) -> List["Template"]:
        """Get the templates that import this one.

        :returns: The list of templates with an ``"import"`` dependency
                  targeting this template.
        """
        found = []

        for t in self.__graph.templates:
            for d in t.get_imports():
                if d.target == Target(False, self.name):
                    found.append(t)

        return found

    def find_children(self) -> List["Template"]:
        """Get the templates extending this one.

        :returns: The list of templates with an ``"extends"`` dependency
                  targeting this template.
        """
        found = []

        for t in self.__graph.templates:
            parent = t.get_parent()
            if parent is not None:
                if parent.target == Target(False, self.name):
                    found.append(t)

        return found


class DependencyGraph:
    """A collection of templates and their dependencies.

    This is the type of the ``dependencies`` attribute of the environment.
    """

    def __init__(self):
        """Initialises a new `DependencyGraph` class.

        This class should not be instanciated manually.
        """
        self.__templates: Dict[str, Template] = {}
        self.__watch_async = False

    def _add_template(self, name: str, file: Optional[str]):
        if name in self.__templates:
            self.__templates[name]._set_modified()
        else:
            self.__templates[name] = Template(name, file, self)

    def _register_dependency(
        self,
        dependent: str,
        dependency_type: str,
        targets: List[Target],
        **kwargs,
    ) -> int:
        dependency = Dependency(dependency_type, targets, **kwargs)

        if dependent not in self.__templates:
            raise ValueError(f"No such tempate: {dependent}")

        return self.__templates[dependent]._add_dependency(dependency)

    def _resolve_dependency(
        self,
        dependent: str,
        dependency_id: int,
        template: jinja2.Template,
    ) -> jinja2.Template:
        if dependent in self.__templates and template.name is not None:
            self.__templates[dependent]._resolve_dependency(
                dependency_id, template.name
            )
        # otherise, ignore silently not to break existing code

        return template

    @property
    def templates(self) -> List[Template]:
        """All the templates known to the environment."""
        return list(self.__templates.values())

    @property
    def watch_async(self) -> bool:
        """See `used_last_watch <#jinja2td.DependencyGraph.used_last_watch>`_."""
        return self.__watch_async

    @watch_async.setter
    def watch_async(self, value: bool):
        self.__watch_async = value

    def get_template(self, name: str) -> Optional[Template]:
        """Get a template.

        :param name: The name of the template, the same you would pass to
                     `jinja2.Environment.get_template <https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment.get_template>`_.

        :returns: The corresponding template, or None if the template is
                  unknown.
        """
        return self.__templates.get(name)

    def watch(self):
        """Start watching for templates used.

        Call it before rendering a template, and then use
        `used_last_watch <#jinja2td.DependencyGraph.used_last_watch>`_
        to get all the templates used to build it.
        """
        for t in self.__templates.values():
            t._watch_reset()

    def used_last_watch(self) -> List[Template]:
        """Returns all the templates used for rendering templates since the last
        call to `watch`.

        By deault, the watch system is disabled in async environments, because
        it gets messy when multiple
        `jinja2.Template.render_async <https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Template.render_async>`_
        run in parallel. You can enable it explicitly by setting
        `watch_async <#jinja2td.DependencyGraph.watch_async>`_ to ``True``, but
        *be careful not to call* `watch <#jinja2td.DependencyGraph.watch>`_ *or*
        `used_last_watch <#jinja2td.DependencyGraph.used_last_watch>`_ *while a
        template is rendering*.

        :returns: The names of the templates used during the last watch.
        """
        since_last_watch = []
        for t in self.__templates.values():
            for d in t.dependencies:
                since_last_watch += d.resolved_last_watch
        return [self.__templates[name] for name in set(since_last_watch)]
