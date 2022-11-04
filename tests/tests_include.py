import unittest

import jinja2
import jinja2td


class TestsInclude(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        files = {
            "variable": r"{{ modelcase }}",
            "nested": r"Modelcase_{% include 'variable' %}",
            "no_includes": r"FIVE_Over Modelcase_RAILGUN",
            "static": r"FIVE_Over Modelcase_{% include 'variable' %}",
            "static_ignore": r"FIVE_Over Modelcase_{% include 'variable' ignore missing %}",
            "static_with": r"FIVE_Over Modelcase_{% include 'variable' with context %}",
            "static_with_ignore": r"FIVE_Over Modelcase_RAILGUN{% include 'variabl' ignore missing with context %}",
            "static_without": r"FIVE_Over Modelcase_RAILGUN{% include 'variable' without context %}",
            "static_multiple": r"FIVE_Over Modelcase_{% include ['variabl', 'variable'] %}",
            "static_nested": r"FIVE_Over {% include 'nested' %}",
            "dynamic": r"FIVE_Over Modelcase_{% include dyn_variable %}",
            "dynamic_ignore": r"FIVE_Over Modelcase_{% include dyn_variable ignore missing %}",
            "dynamic_with": r"FIVE_Over Modelcase_{% include dyn_variable with context %}",
            "dynamic_with_ignore": r"FIVE_Over Modelcase_RAILGUN{% include dyn_wrong ignore missing with context %}",
            "dynamic_without": r"FIVE_Over Modelcase_RAILGUN{% include dyn_variable without context %}",
            "dynamic_multiple": r"FIVE_Over Modelcase_{% include ('variabl', dyn_variable) %}",
            "dynamic_nested": r"FIVE_Over {% include dyn_nested %}",
        }

        cls.env = jinja2.Environment(
            loader=jinja2.DictLoader(files),
            extensions=[jinja2td.Introspection],
        )

        cls.data = {
            "modelcase": "RAILGUN",
            "dyn_variable": "variable",
            "dyn_wrong": "variabl",
            "dyn_nested": "nested",
        }

    def test_no_includes(self):
        template = TestsInclude.env.get_template("no_includes")

        result = template.render(TestsInclude.data)

        self.assertEqual("FIVE_Over Modelcase_RAILGUN", result)

        dependencies = TestsInclude.env.dependencies.get_template(
            "no_includes"
        ).dependencies

        self.assertEqual(0, len(dependencies))

    def test_static(self):
        template = TestsInclude.env.get_template("static")

        result = template.render(TestsInclude.data)

        self.assertEqual("FIVE_Over Modelcase_RAILGUN", result)

        dependencies = TestsInclude.env.dependencies.get_template("static").dependencies

        self.assertEqual(1, len(dependencies))

        self.assertIsNot(None, dependencies[0].target)

        self.assertFalse(dependencies[0].target.is_dynamic)
        self.assertEqual("variable", dependencies[0].target.name)

        self.assertTrue(dependencies[0].with_context)
        self.assertFalse(dependencies[0].ignore_missing)

    def test_static_ignore(self):
        template = TestsInclude.env.get_template("static_ignore")

        result = template.render(TestsInclude.data)

        self.assertEqual("FIVE_Over Modelcase_RAILGUN", result)

        dependencies = TestsInclude.env.dependencies.get_template(
            "static_ignore"
        ).dependencies

        self.assertEqual(1, len(dependencies))

        self.assertIsNot(None, dependencies[0].target)

        self.assertFalse(dependencies[0].target.is_dynamic)
        self.assertEqual("variable", dependencies[0].target.name)

        self.assertTrue(dependencies[0].with_context)
        self.assertTrue(dependencies[0].ignore_missing)

    def test_static_with(self):
        template = TestsInclude.env.get_template("static_with")

        result = template.render(TestsInclude.data)

        self.assertEqual("FIVE_Over Modelcase_RAILGUN", result)

        dependencies = TestsInclude.env.dependencies.get_template(
            "static_with"
        ).dependencies

        self.assertEqual(1, len(dependencies))

        self.assertIsNot(None, dependencies[0].target)

        self.assertFalse(dependencies[0].target.is_dynamic)
        self.assertEqual("variable", dependencies[0].target.name)

        self.assertTrue(dependencies[0].with_context)
        self.assertFalse(dependencies[0].ignore_missing)

    def test_static_with_ignore(self):
        template = TestsInclude.env.get_template("static_with_ignore")

        result = template.render(TestsInclude.data)

        self.assertEqual("FIVE_Over Modelcase_RAILGUN", result)

        dependencies = TestsInclude.env.dependencies.get_template(
            "static_with_ignore"
        ).dependencies

        self.assertEqual(1, len(dependencies))

        self.assertIsNot(None, dependencies[0].target)

        self.assertFalse(dependencies[0].target.is_dynamic)
        self.assertEqual("variabl", dependencies[0].target.name)

        self.assertTrue(dependencies[0].with_context)
        self.assertTrue(dependencies[0].ignore_missing)

    def test_static_without(self):
        template = TestsInclude.env.get_template("static_without")

        result = template.render(TestsInclude.data)

        self.assertEqual("FIVE_Over Modelcase_RAILGUN", result)

        dependencies = TestsInclude.env.dependencies.get_template(
            "static_without"
        ).dependencies

        self.assertEqual(1, len(dependencies))

        self.assertIsNot(None, dependencies[0].target)

        self.assertFalse(dependencies[0].target.is_dynamic)
        self.assertEqual("variable", dependencies[0].target.name)

        self.assertFalse(dependencies[0].with_context)
        self.assertFalse(dependencies[0].ignore_missing)

    def test_static_multiple(self):
        template = TestsInclude.env.get_template("static_multiple")

        result = template.render(TestsInclude.data)

        self.assertEqual("FIVE_Over Modelcase_RAILGUN", result)

        dependencies = TestsInclude.env.dependencies.get_template(
            "static_multiple"
        ).dependencies

        self.assertEqual(1, len(dependencies))

        self.assertEqual(2, len(dependencies[0].targets))

        self.assertFalse(dependencies[0].targets[0].is_dynamic)
        self.assertEqual("variabl", dependencies[0].targets[0].name)

        self.assertFalse(dependencies[0].targets[1].is_dynamic)
        self.assertEqual("variable", dependencies[0].targets[1].name)

        self.assertTrue(dependencies[0].with_context)
        self.assertFalse(dependencies[0].ignore_missing)

    def test_static_nested(self):
        template = TestsInclude.env.get_template("static_nested")

        result = template.render(TestsInclude.data)

        self.assertEqual("FIVE_Over Modelcase_RAILGUN", result)

        dependencies = TestsInclude.env.dependencies.get_template(
            "static_nested"
        ).dependencies

        self.assertEqual(1, len(dependencies))

        self.assertIsNot(None, dependencies[0].target)

        self.assertFalse(dependencies[0].target.is_dynamic)
        self.assertEqual("nested", dependencies[0].target.name)

        self.assertTrue(dependencies[0].with_context)
        self.assertFalse(dependencies[0].ignore_missing)

    def test_dynamic(self):
        template = TestsInclude.env.get_template("dynamic")

        result = template.render(TestsInclude.data)

        self.assertEqual("FIVE_Over Modelcase_RAILGUN", result)

        dependencies = TestsInclude.env.dependencies.get_template(
            "dynamic"
        ).dependencies

        self.assertEqual(1, len(dependencies))

        self.assertIsNot(None, dependencies[0].target)

        self.assertTrue(dependencies[0].target.is_dynamic)
        self.assertIs(None, dependencies[0].target.name)

        self.assertTrue(dependencies[0].with_context)
        self.assertFalse(dependencies[0].ignore_missing)

    def test_dynamic_ignore(self):
        template = TestsInclude.env.get_template("dynamic_ignore")

        result = template.render(TestsInclude.data)

        self.assertEqual("FIVE_Over Modelcase_RAILGUN", result)

        dependencies = TestsInclude.env.dependencies.get_template(
            "dynamic_ignore"
        ).dependencies

        self.assertEqual(1, len(dependencies))

        self.assertIsNot(None, dependencies[0].target)

        self.assertTrue(dependencies[0].target.is_dynamic)
        self.assertIs(None, dependencies[0].target.name)

        self.assertTrue(dependencies[0].with_context)
        self.assertTrue(dependencies[0].ignore_missing)

    def test_dynamic_with(self):
        template = TestsInclude.env.get_template("dynamic_with")

        result = template.render(TestsInclude.data)

        self.assertEqual("FIVE_Over Modelcase_RAILGUN", result)

        dependencies = TestsInclude.env.dependencies.get_template(
            "dynamic_with"
        ).dependencies

        self.assertEqual(1, len(dependencies))

        self.assertIsNot(None, dependencies[0].target)

        self.assertTrue(dependencies[0].target.is_dynamic)
        self.assertIs(None, dependencies[0].target.name)

        self.assertTrue(dependencies[0].with_context)
        self.assertFalse(dependencies[0].ignore_missing)

    def test_dynamic_with_ignore(self):
        template = TestsInclude.env.get_template("dynamic_with_ignore")

        result = template.render(TestsInclude.data)

        self.assertEqual("FIVE_Over Modelcase_RAILGUN", result)

        dependencies = TestsInclude.env.dependencies.get_template(
            "dynamic_with_ignore"
        ).dependencies

        self.assertEqual(1, len(dependencies))

        self.assertIsNot(None, dependencies[0].target)

        self.assertTrue(dependencies[0].target.is_dynamic)
        self.assertIs(None, dependencies[0].target.name)

        self.assertTrue(dependencies[0].with_context)
        self.assertTrue(dependencies[0].ignore_missing)

    def test_dynamic_without(self):
        template = TestsInclude.env.get_template("dynamic_without")

        result = template.render(TestsInclude.data)

        self.assertEqual("FIVE_Over Modelcase_RAILGUN", result)

        dependencies = TestsInclude.env.dependencies.get_template(
            "dynamic_without"
        ).dependencies

        self.assertEqual(1, len(dependencies))

        self.assertIsNot(None, dependencies[0].target)

        self.assertTrue(dependencies[0].target.is_dynamic)
        self.assertIs(None, dependencies[0].target.name)

        self.assertFalse(dependencies[0].with_context)
        self.assertFalse(dependencies[0].ignore_missing)

    def test_dynamic_multiple(self):
        template = TestsInclude.env.get_template("dynamic_multiple")

        result = template.render(TestsInclude.data)

        self.assertEqual("FIVE_Over Modelcase_RAILGUN", result)

        dependencies = TestsInclude.env.dependencies.get_template(
            "dynamic_multiple"
        ).dependencies

        self.assertEqual(1, len(dependencies))

        self.assertEqual(2, len(dependencies[0].targets))

        self.assertFalse(dependencies[0].targets[0].is_dynamic)
        self.assertEqual("variabl", dependencies[0].targets[0].name)

        self.assertTrue(dependencies[0].targets[1].is_dynamic)
        self.assertIs(None, dependencies[0].targets[1].name)

        self.assertTrue(dependencies[0].with_context)
        self.assertFalse(dependencies[0].ignore_missing)

    def test_dynamic_nested(self):
        template = TestsInclude.env.get_template("dynamic_nested")

        result = template.render(TestsInclude.data)

        self.assertEqual("FIVE_Over Modelcase_RAILGUN", result)

        dependencies = TestsInclude.env.dependencies.get_template(
            "dynamic_nested"
        ).dependencies

        self.assertEqual(1, len(dependencies))

        self.assertIsNot(None, dependencies[0].target)

        self.assertTrue(dependencies[0].target.is_dynamic)
        self.assertIs(None, dependencies[0].target.name)

        self.assertTrue(dependencies[0].with_context)
        self.assertFalse(dependencies[0].ignore_missing)

    def test_get_includes(self):
        # just make sure the necessary templates are loaded
        TestsInclude.env.get_template("static_nested")

        template = TestsInclude.env.dependencies.get_template("static_nested")

        includes = template.get_includes()

        self.assertEqual(1, len(includes))

        self.assertIsNot(None, includes[0].target)

        self.assertFalse(includes[0].target.is_dynamic)
        self.assertEqual("nested", includes[0].target.name)

        self.assertTrue(includes[0].with_context)
        self.assertFalse(includes[0].ignore_missing)

    def test_find_included(self):
        # just make sure the necessary templates are loaded
        TestsInclude.env.get_template("static_nested")
        TestsInclude.env.get_template("dynamic_nested")

        static_nested = TestsInclude.env.dependencies.get_template("static_nested")
        nested = TestsInclude.env.dependencies.get_template("nested")

        nested_includes = nested.find_included()

        self.assertEqual(1, len(nested_includes))

        self.assertIs(static_nested, nested_includes[0])

        # dynamic_nested isn't found because it is dynamic
