"""Alter the behavior of the Jinja template compiler. 
"""
from jinja2.compiler import CodeGenerator, Frame, t, CompilerExit
from jinja2 import nodes

from .dependencies import Target


def _override(cls):
    def deco(func):
        docstring = getattr(cls, func.__name__).__doc__
        if docstring is None:
            docstring = ""
        else:
            docstring += "\n\n"
        func.__doc__ = docstring + "(Warning: this method has been altered by jinja2td)"
        setattr(cls, func.__name__, func)

    return deco


@_override(CodeGenerator)
def visit_Include(self, node: nodes.Include, frame: Frame) -> None:
    # The code in this section is has been copied verbatim from Jinja2 (file compiler.py, lines 1031 to 1055)
    # https://github.com/pallets/jinja/blob/b08cd4bc64bb980df86ed2876978ae5735572280/src/jinja2/compiler.py#L1031-L1055
    # Copyright 2007 Pallets - This code is licensed under the BSD 3-Clause license.
    # See LICENSE_JINJA2 for the full license text.
    # BEGIN COPIED CODE
    if node.ignore_missing:
        self.writeline("try:")
        self.indent()

    func_name = "get_or_select_template"
    if isinstance(node.template, nodes.Const):
        if isinstance(node.template.value, str):
            func_name = "get_template"
        elif isinstance(node.template.value, (tuple, list)):
            func_name = "select_template"
    elif isinstance(node.template, (nodes.Tuple, nodes.List)):
        func_name = "select_template"

    self.writeline(f"template = environment.{func_name}(", node)
    self.visit(node.template, frame)
    self.write(f", {self.name!r})")
    if node.ignore_missing:
        self.outdent()
        self.writeline("except TemplateNotFound:")
        self.indent()
        self.writeline("pass")
        self.outdent()
        self.writeline("else:")
        self.indent()
    # END COPIED CODE

    if hasattr(self.environment, "dependencies"):
        targets = [Target(True, None)]
        if isinstance(node.template, nodes.Const):
            if isinstance(node.template.value, str):
                targets = [Target(False, node.template.value)]
            elif isinstance(node.template.value, (tuple, list)):
                targets = [Target(False, name) for name in node.template.value]
        elif isinstance(node.template, (nodes.Tuple, nodes.List)):
            targets = [
                Target(False, item.value)
                if (isinstance(item, nodes.Const) and isinstance(item.value, str))
                else Target(True, None)
                for item in node.template.items
            ]

        dependency_id = self.environment.dependencies._register_dependency(
            dependent=self.name,
            dependency_type="include",
            targets=targets,
            with_context=node.with_context,
            ignore_missing=node.ignore_missing,
        )

        # tracking templates in async environments could break the watch system
        if not self.environment.is_async or self.environment.dependencies.watch_async:
            self.writeline("if hasattr(environment, 'dependencies'):")
            self.indent()
            self.writeline(
                f"environment.dependencies._resolve_dependency({self.name!r}, {dependency_id}, template)"
            )
            self.outdent()

    # The code in this section is has been copied verbatim from Jinja2 (file compiler.py, lines 1057 to 1079)
    # https://github.com/pallets/jinja/blob/b08cd4bc64bb980df86ed2876978ae5735572280/src/jinja2/compiler.py#L1057-L1079
    # Copyright 2007 Pallets - This code is licensed under the BSD 3-Clause license.
    # See LICENSE_JINJA2 for the full license text.
    # BEGIN COPIED CODE
    skip_event_yield = False
    if node.with_context:
        self.writeline(
            f"{self.choose_async()}for event in template.root_render_func("
            "template.new_context(context.get_all(), True,"
            f" {self.dump_local_context(frame)})):"
        )
    elif self.environment.is_async:
        self.writeline(
            "for event in (await template._get_default_module_async())" "._body_stream:"
        )
    else:
        self.writeline("yield from template._get_default_module()._body_stream")
        skip_event_yield = True

    if not skip_event_yield:
        self.indent()
        self.simple_write("event", frame)
        self.outdent()

    if node.ignore_missing:
        self.outdent()
    # END COPIED CODE


@_override(CodeGenerator)
def _import_common(
    self,
    node: t.Union[nodes.Import, nodes.FromImport],
    frame: Frame,
) -> None:
    if hasattr(self.environment, "dependencies"):
        targets = [Target(True, None)]
        if isinstance(node.template, nodes.Const):
            if isinstance(node.template.value, str):
                targets = [Target(False, node.template.value)]

        dependency_id = self.environment.dependencies._register_dependency(
            dependent=self.name,
            dependency_type="import",
            targets=targets,
            with_context=node.with_context,
            imported_as=node.target if isinstance(node, nodes.Import) else None,
            imported_names=node.names if isinstance(node, nodes.FromImport) else None,
        )

        # tracking templates in async environments could break the watch system
        if not self.environment.is_async or self.environment.dependencies.watch_async:
            self.write("(lambda template: ")
            self.write(
                f"environment.dependencies._resolve_dependency({self.name!r}, {dependency_id}, template)"
            )
            self.write(" if hasattr(environment, 'dependencies') else template)(")

    # The code in this section is has been copied verbatim from Jinja2 (file compiler.py, lines 1084 to 1085)
    # https://github.com/pallets/jinja/blob/b08cd4bc64bb980df86ed2876978ae5735572280/src/jinja2/compiler.py#L1084-L1085
    # Copyright 2007 Pallets - This code is licensed under the BSD 3-Clause license.
    # See LICENSE_JINJA2 for the full license text.
    # BEGIN COPIED CODE
    self.write(f"{self.choose_async('await ')}environment.get_template(")
    self.visit(node.template, frame)
    # END COPIED CODE

    self.write(f", {self.name!r})")
    if hasattr(self.environment, "dependencies"):
        if not self.environment.is_async or self.environment.dependencies.watch_async:
            self.write(")")  # close the parenthesis open at the and of line 144
    self.write(".")

    # The code in this section is has been copied verbatim from Jinja2 (file compiler.py, lines 1088 to 1094)
    # https://github.com/pallets/jinja/blob/b08cd4bc64bb980df86ed2876978ae5735572280/src/jinja2/compiler.py#L1088-L1094
    # Copyright 2007 Pallets - This code is licensed under the BSD 3-Clause license.
    # See LICENSE_JINJA2 for the full license text.
    # BEGIN COPIED CODE
    if node.with_context:
        f_name = f"make_module{self.choose_async('_async')}"
        self.write(
            f"{f_name}(context.get_all(), True, {self.dump_local_context(frame)})"
        )
    else:
        self.write(f"_get_default_module{self.choose_async('_async')}(context)")
    # END COPIED CODE


@_override(CodeGenerator)
def visit_Extends(self, node: nodes.Extends, frame: Frame) -> None:
    # The code in this section is has been copied verbatim from Jinja2 (file compiler.py, lines 989 to 1015)
    # https://github.com/pallets/jinja/blob/b08cd4bc64bb980df86ed2876978ae5735572280/src/jinja2/compiler.py#L989-L1015
    # Copyright 2007 Pallets - This code is licensed under the BSD 3-Clause license.
    # See LICENSE_JINJA2 for the full license text.
    # BEGIN COPIED CODE
    if not frame.toplevel:
        self.fail("cannot use extend from a non top-level scope", node.lineno)

    # if the number of extends statements in general is zero so
    # far, we don't have to add a check if something extended
    # the template before this one.
    if self.extends_so_far > 0:

        # if we have a known extends we just add a template runtime
        # error into the generated code.  We could catch that at compile
        # time too, but i welcome it not to confuse users by throwing the
        # same error at different times just "because we can".
        if not self.has_known_extends:
            self.writeline("if parent_template is not None:")
            self.indent()
        self.writeline('raise TemplateRuntimeError("extended multiple times")')

        # if we have a known extends already we don't need that code here
        # as we know that the template execution will end here.
        if self.has_known_extends:
            raise CompilerExit()
        else:
            self.outdent()

    self.writeline("parent_template = environment.get_template(", node)
    self.visit(node.template, frame)
    self.write(f", {self.name!r})")
    # END COPIED CODE

    if hasattr(self.environment, "dependencies"):
        targets = [Target(True, None)]
        if isinstance(node.template, nodes.Const):
            if isinstance(node.template.value, str):
                targets = [Target(False, node.template.value)]

        dependency_id = self.environment.dependencies._register_dependency(
            dependent=self.name,
            dependency_type="extends",
            targets=targets,
        )

        # tracking templates in async environments could break the watch system
        if not self.environment.is_async or self.environment.dependencies.watch_async:
            self.writeline("if hasattr(environment, 'dependencies'):")
            self.indent()
            self.writeline(
                f"environment.dependencies._resolve_dependency({self.name!r}, {dependency_id}, parent_template)"
            )
            self.outdent()

    # The code in this section is has been copied verbatim from Jinja2 (file compiler.py, lines 1016 to 1028)
    # https://github.com/pallets/jinja/blob/b08cd4bc64bb980df86ed2876978ae5735572280/src/jinja2/compiler.py#L1015-L1028
    # Copyright 2007 Pallets - This code is licensed under the BSD 3-Clause license.
    # See LICENSE_JINJA2 for the full license text.
    # BEGIN COPIED CODE
    self.writeline("for name, parent_block in parent_template.blocks.items():")
    self.indent()
    self.writeline("context.blocks.setdefault(name, []).append(parent_block)")
    self.outdent()

    # if this extends statement was in the root level we can take
    # advantage of that information and simplify the generated code
    # in the top level from this point onwards
    if frame.rootlevel:
        self.has_known_extends = True

    # and now we have one more
    self.extends_so_far += 1
    # END COPIED CODE
