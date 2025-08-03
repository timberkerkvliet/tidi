from unittest import TestCase

from test_tidi import context_composition
from test_tidi.context_composition import StringGenerator, HelloGenerator, TimberGenerator, App
from tidi import scan, get_resolver, reset, add_context, ensure_scope


class TestContext(TestCase):
    def setUp(self) -> None:
        scan(context_composition)
        self.resolver = get_resolver()

    def tearDown(self) -> None:
        reset()

    def test_production(self):
        add_context(environment='prod')
        result = self.resolver(StringGenerator)

        self.assertEqual(result.generate(), 'Timber')

    def test_specific_type(self):
        add_context(environment='test')
        result = self.resolver(HelloGenerator)

        self.assertEqual(result.generate(), 'Hello')

    def test_resolves_with_additional_values(self):
        add_context(environment='test', some_extra_key='iets')
        result = self.resolver(HelloGenerator)

        self.assertEqual(result.generate(), 'Hello')

    def test_cannot_resolve_with_multiple_candidates(self):
        with self.assertRaises(Exception):
            self.resolver(StringGenerator)

    def test_can_resolve_specific(self):
        result = self.resolver(TimberGenerator)

        self.assertEqual(result.generate(), 'Timber')

    def test_resolve_app(self):
        add_context(environment='test')
        app = self.resolver(App)

        self.assertEqual(app.generate(), 'Hello')

    def test_cannot_change_context(self):
        add_context(environment='test')

        with self.assertRaises(Exception):
            add_context(environment='prod')

    def test_cannot_change_context_in_child(self):
        add_context(environment='test')
        ensure_scope('child', scope_type='child')

        with self.assertRaises(Exception):
            add_context('child', environment='prod')

    def test_adding_context_to_child_scope_does_not_influence_root(self):
        ensure_scope(scope_id='child', scope_type='child')
        add_context(scope_id='child', environment='test')
        root_resolver = get_resolver()
        child_resolver = get_resolver('child')

        with self.assertRaises(Exception):
            root_resolver(StringGenerator)
        with self.assertRaises(Exception):
            child_resolver(StringGenerator)
