import unittest

import jinja2
import jinja2td


class TestsExtends(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        files = {
            "root": r"FIVE_Over Modelcase_{% block railgun %}RAILGUN{% endblock %}",
            "static": r"{% extends 'root' %}",
            "dynamic": r"{% extends root %}{% block railgun %}{{ railgun }}{% endblock %}",
            "indirect": r"{% extends 'static' %}{% block railgun %}{{ railgun }}{% endblock %}",
        }

        cls.env = jinja2.Environment(
            loader=jinja2.DictLoader(files),
            extensions=[jinja2td.Introspection],
        )

        cls.data = {"root": "root", "railgun": "RAILGUN"}

    def test_root(self):
        template = TestsExtends.env.get_template("root")

        result = template.render(TestsExtends.data)

        self.assertEqual("FIVE_Over Modelcase_RAILGUN", result)

        dependencies = TestsExtends.env.dependencies.get_template("root").dependencies

        self.assertEqual(0, len(dependencies))

    def test_static(self):
        template = TestsExtends.env.get_template("static")

        result = template.render(TestsExtends.data)

        self.assertEqual("FIVE_Over Modelcase_RAILGUN", result)

        dependencies = TestsExtends.env.dependencies.get_template("static").dependencies

        self.assertEqual(1, len(dependencies))

        self.assertIsNot(None, dependencies[0].target)

        self.assertFalse(dependencies[0].target.is_dynamic)
        self.assertEqual("root", dependencies[0].target.name)

    def test_dynamic(self):
        template = TestsExtends.env.get_template("dynamic")

        result = template.render(TestsExtends.data)

        self.assertEqual("FIVE_Over Modelcase_RAILGUN", result)

        dependencies = TestsExtends.env.dependencies.get_template(
            "dynamic"
        ).dependencies

        self.assertEqual(1, len(dependencies))

        self.assertIsNot(None, dependencies[0].target)

        self.assertTrue(dependencies[0].target.is_dynamic)
        self.assertIs(None, dependencies[0].target.name)

    def test_indirect(self):
        template = TestsExtends.env.get_template("indirect")

        result = template.render(TestsExtends.data)

        self.assertEqual("FIVE_Over Modelcase_RAILGUN", result)

        dependencies = TestsExtends.env.dependencies.get_template(
            "indirect"
        ).dependencies

        self.assertEqual(1, len(dependencies))

        self.assertIsNot(None, dependencies[0].target)

        self.assertFalse(dependencies[0].target.is_dynamic)
        self.assertEqual("static", dependencies[0].target.name)

    def test_get_parent(self):
        # just make sure the necessary templates are loaded
        TestsExtends.env.get_template("root")
        TestsExtends.env.get_template("static")

        root = TestsExtends.env.dependencies.get_template("root")
        static = TestsExtends.env.dependencies.get_template("static")

        self.assertIs(None, root.get_parent())

        static_parent = static.get_parent()

        self.assertIsNot(None, static_parent)
        self.assertIsNot(None, static_parent.target)
        self.assertEqual("root", static_parent.target.name)

    def test_find_children(self):
        # just make sure the necessary templates are loaded
        TestsExtends.env.get_template("root")
        TestsExtends.env.get_template("static")
        TestsExtends.env.get_template("dynamic")

        root = TestsExtends.env.dependencies.get_template("root")
        static = TestsExtends.env.dependencies.get_template("static")
        dynamic = TestsExtends.env.dependencies.get_template("dynamic")

        children = root.find_children()

        self.assertEqual(1, len(children))

        self.assertIs(static, children[0])

        # dynamic isn't found because it is dynamic
