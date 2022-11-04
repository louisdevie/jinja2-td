import unittest

import jinja2
import jinja2td


class TestsImport(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        files = {
            "macros": (
                r"{% macro modelcase(ability) %}Modelcase_{{ ability | upper }}{% endmacro %}"
                "{% macro modelcase2() %}Modelcase_{{ railgun }}{% endmacro %}"
            ),
            "no_imports": r"FIVE_Over Modelcase_RAILGUN",
            "static": r"{% import 'macros' as m %}FIVE_Over {{ m.modelcase('Railgun') }}",
            "static_from": r"{% from 'macros' import modelcase %}FIVE_Over {{ modelcase('Railgun') }}",
            "static_with": r"{% import 'macros' as m with context %}FIVE_Over {{ m.modelcase2() }}",
            "static_with_from": r"{% from 'macros' import modelcase2 with context %}FIVE_Over {{ modelcase2() }}",
            "dynamic": r"{% import dyn_macros as m %}FIVE_Over {{ m.modelcase('Railgun') }}",
            "dynamic_from": r"{% from dyn_macros import modelcase %}FIVE_Over {{ modelcase('Railgun') }}",
            "dynamic_with": r"{% import dyn_macros as m with context %}FIVE_Over {{ m.modelcase2() }}",
            "dynamic_with_from": r"{% from dyn_macros import modelcase2 with context %}FIVE_Over {{ modelcase2() }}",
        }

        cls.env = jinja2.Environment(
            loader=jinja2.DictLoader(files),
            extensions=[jinja2td.Introspection],
        )

        cls.data = {
            "railgun": "RAILGUN",
            "dyn_macros": "macros",
        }

    def test_no_imports(self):
        template = TestsImport.env.get_template("no_imports")

        result = template.render(TestsImport.data)

        self.assertEqual("FIVE_Over Modelcase_RAILGUN", result)

        dependencies = TestsImport.env.dependencies.get_template(
            "no_imports"
        ).dependencies

        self.assertEqual(0, len(dependencies))

    def test_static(self):
        template = TestsImport.env.get_template("static")

        result = template.render(TestsImport.data)

        self.assertEqual("FIVE_Over Modelcase_RAILGUN", result)

        dependencies = TestsImport.env.dependencies.get_template("static").dependencies

        self.assertEqual(1, len(dependencies))

        self.assertIsNot(None, dependencies[0].target)

        self.assertFalse(dependencies[0].target.is_dynamic)
        self.assertEqual("macros", dependencies[0].target.name)

        self.assertFalse(dependencies[0].with_context)
        self.assertEqual("m", dependencies[0].imported_as)
        self.assertIs(None, dependencies[0].imported_names)

    def test_static_from(self):
        template = TestsImport.env.get_template("static_from")

        result = template.render(TestsImport.data)

        self.assertEqual("FIVE_Over Modelcase_RAILGUN", result)

        dependencies = TestsImport.env.dependencies.get_template(
            "static_from"
        ).dependencies

        self.assertEqual(1, len(dependencies))

        self.assertIsNot(None, dependencies[0].target)

        self.assertFalse(dependencies[0].target.is_dynamic)
        self.assertEqual("macros", dependencies[0].target.name)

        self.assertFalse(dependencies[0].with_context)
        self.assertIs(None, dependencies[0].imported_as)
        self.assertEqual(["modelcase"], dependencies[0].imported_names)

    def test_static_with(self):
        template = TestsImport.env.get_template("static_with")

        result = template.render(TestsImport.data)

        self.assertEqual("FIVE_Over Modelcase_RAILGUN", result)

        dependencies = TestsImport.env.dependencies.get_template(
            "static_with"
        ).dependencies

        self.assertEqual(1, len(dependencies))

        self.assertIsNot(None, dependencies[0].target)

        self.assertFalse(dependencies[0].target.is_dynamic)
        self.assertEqual("macros", dependencies[0].target.name)

        self.assertTrue(dependencies[0].with_context)
        self.assertEqual("m", dependencies[0].imported_as)
        self.assertIs(None, dependencies[0].imported_names)

    def test_static_with_from(self):
        template = TestsImport.env.get_template("static_with_from")

        result = template.render(TestsImport.data)

        self.assertEqual("FIVE_Over Modelcase_RAILGUN", result)

        dependencies = TestsImport.env.dependencies.get_template(
            "static_with_from"
        ).dependencies

        self.assertEqual(1, len(dependencies))

        self.assertIsNot(None, dependencies[0].target)

        self.assertFalse(dependencies[0].target.is_dynamic)
        self.assertEqual("macros", dependencies[0].target.name)

        self.assertTrue(dependencies[0].with_context)
        self.assertIs(None, dependencies[0].imported_as)
        self.assertEqual(["modelcase2"], dependencies[0].imported_names)

    def test_dynamic(self):
        template = TestsImport.env.get_template("dynamic")

        result = template.render(TestsImport.data)

        self.assertEqual("FIVE_Over Modelcase_RAILGUN", result)

        dependencies = TestsImport.env.dependencies.get_template("dynamic").dependencies

        self.assertEqual(1, len(dependencies))

        self.assertIsNot(None, dependencies[0].target)

        self.assertTrue(dependencies[0].target.is_dynamic)
        self.assertIs(None, dependencies[0].target.name)

        self.assertFalse(dependencies[0].with_context)
        self.assertEqual("m", dependencies[0].imported_as)
        self.assertIs(None, dependencies[0].imported_names)

    def test_dynamic_from(self):
        template = TestsImport.env.get_template("dynamic_from")

        result = template.render(TestsImport.data)

        self.assertEqual("FIVE_Over Modelcase_RAILGUN", result)

        dependencies = TestsImport.env.dependencies.get_template(
            "dynamic_from"
        ).dependencies

        self.assertEqual(1, len(dependencies))

        self.assertIsNot(None, dependencies[0].target)

        self.assertTrue(dependencies[0].target.is_dynamic)
        self.assertIs(None, dependencies[0].target.name)

        self.assertFalse(dependencies[0].with_context)
        self.assertIs(None, dependencies[0].imported_as)
        self.assertEqual(["modelcase"], dependencies[0].imported_names)

    def test_dynamic_with(self):
        template = TestsImport.env.get_template("dynamic_with")

        result = template.render(TestsImport.data)

        self.assertEqual("FIVE_Over Modelcase_RAILGUN", result)

        dependencies = TestsImport.env.dependencies.get_template(
            "dynamic_with"
        ).dependencies

        self.assertEqual(1, len(dependencies))

        self.assertIsNot(None, dependencies[0].target)

        self.assertTrue(dependencies[0].target.is_dynamic)
        self.assertIs(None, dependencies[0].target.name)

        self.assertTrue(dependencies[0].with_context)
        self.assertEqual("m", dependencies[0].imported_as)
        self.assertIs(None, dependencies[0].imported_names)

    def test_dynamic_with_from(self):
        template = TestsImport.env.get_template("dynamic_with_from")

        result = template.render(TestsImport.data)

        self.assertEqual("FIVE_Over Modelcase_RAILGUN", result)

        dependencies = TestsImport.env.dependencies.get_template(
            "dynamic_with_from"
        ).dependencies

        self.assertEqual(1, len(dependencies))

        self.assertIsNot(None, dependencies[0].target)

        self.assertTrue(dependencies[0].target.is_dynamic)
        self.assertIs(None, dependencies[0].target.name)

        self.assertTrue(dependencies[0].with_context)
        self.assertIs(None, dependencies[0].imported_as)
        self.assertEqual(["modelcase2"], dependencies[0].imported_names)

    def test_get_imports(self):
        # just make sure the necessary templates are loaded
        TestsImport.env.get_template("static")

        template = TestsImport.env.dependencies.get_template("static")

        imports = template.get_imports()

        self.assertEqual(1, len(imports))

        self.assertIsNot(None, imports[0].target)

        self.assertFalse(imports[0].target.is_dynamic)
        self.assertEqual("macros", imports[0].target.name)

        self.assertFalse(imports[0].with_context)
        self.assertEqual("m", imports[0].imported_as)
        self.assertIs(None, imports[0].imported_names)

    def test_find_imported(self):
        # just make sure the necessary templates are loaded
        TestsImport.env.get_template("macros")
        TestsImport.env.get_template("static")
        TestsImport.env.get_template("dynamic")

        macros = TestsImport.env.dependencies.get_template("macros")
        static = TestsImport.env.dependencies.get_template("static")
        dynamic = TestsImport.env.dependencies.get_template("dynamic")

        macros_imports = macros.find_imported()

        self.assertIn(static, macros_imports)

        # dynamic imports aren't found because they're dynamic
        self.assertNotIn(dynamic, macros_imports)
