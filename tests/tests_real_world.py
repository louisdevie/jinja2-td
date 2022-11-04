import unittest

import jinja2
import jinja2td

from path_setup import TESTS_DIR


class TestsRealWorld(unittest.TestCase):
    def test_without_jinja2td(self):
        # check that we did not broke anything
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(TESTS_DIR))

        template2 = env.get_template("template2.j2")

        result2 = template2.render(
            is_outsider=True, dynamic_include="template3.j2", modelcase="MENTALOUT"
        )

        self.assertEqual(result2, "FIVE_Over OS Modelcase_MENTALOUT")

    def test_with_jinja2td(self):
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(TESTS_DIR),
            extensions=[jinja2td.Introspection],
        )

        template2 = env.get_template("template2.j2")

        env.dependencies.watch()
        result2 = template2.render(
            is_outsider=True, dynamic_include="template3.j2", modelcase="MENTALOUT"
        )
        all_templates = env.dependencies.used_last_watch()

        self.assertEqual(result2, "FIVE_Over OS Modelcase_MENTALOUT")

        t1 = env.dependencies.get_template("template1.j2")
        t2 = env.dependencies.get_template("template2.j2")
        t3 = env.dependencies.get_template("template3.j2")
        t4 = env.dependencies.get_template("template4.j2")

        self.assertEqual(t1.file, str(TESTS_DIR / "template1.j2"))
        self.assertEqual(t2.file, str(TESTS_DIR / "template2.j2"))
        self.assertEqual(t3.file, str(TESTS_DIR / "template3.j2"))
        self.assertEqual(t4.file, str(TESTS_DIR / "template4.j2"))

        # the order is not important
        self.assertEqual(3, len(all_templates))
        self.assertIn(t1, all_templates)
        # the template rendered isn't a dependency
        self.assertIn(t3, all_templates)
        self.assertIn(t4, all_templates)
