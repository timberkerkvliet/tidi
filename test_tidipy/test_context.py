from unittest import TestCase

from test_tidipy import context_composition
from test_tidipy.context_composition import StringGenerator, HelloGenerator, TimberGenerator, App
from tidipy import scan, get_resolver, reset, ensure_scope


class TestContext(TestCase):
    def setUp(self) -> None:
        scan(context_composition)

    def tearDown(self) -> None:
        reset()

    def test_production(self):
        ensure_scope(scope_id='app-prod', scope_type='app', context={'environment': 'prod'})
        result = get_resolver('app-prod')(StringGenerator)

        self.assertEqual(result.generate(), 'Timber')

    def test_specific_type(self):
        ensure_scope(scope_id='app', scope_type='app', context={'environment': 'test'})
        result = get_resolver('app')(HelloGenerator)

        self.assertEqual(result.generate(), 'Hello')

    def test_resolves_with_additional_values(self):
        ensure_scope(scope_id='app', scope_type='app', context={'environment': 'test', 'a': 'b'})
        result = get_resolver('app')(HelloGenerator)

        self.assertEqual(result.generate(), 'Hello')

    def test_cannot_resolve_with_multiple_candidates(self):
        with self.assertRaises(Exception):
            get_resolver()(StringGenerator)

    def test_can_resolve_specific(self):
        ensure_scope(scope_id='app', scope_type='app', context={'environment': 'prod'})
        result = get_resolver('app')(TimberGenerator)

        self.assertEqual(result.generate(), 'Timber')

    def test_resolve_app(self):
        ensure_scope(scope_id='app', scope_type='app', context={'environment': 'test'})
        app = get_resolver('app')(App)

        self.assertEqual(app.generate(), 'Hello')

    def test_resolve_two_apps(self):
        ensure_scope(scope_id='app-test', scope_type='app', context={'environment': 'test'})
        ensure_scope(scope_id='app-prod', scope_type='app', context={'environment': 'prod'})
        prod_app = get_resolver('app-prod')(App)
        test_app = get_resolver('app-test')(App)

        self.assertEqual(test_app.generate(), 'Hello')
        self.assertEqual(prod_app.generate(), 'Timber')

    def test_cannot_change_context(self):
        ensure_scope(scope_id='app', scope_type='app', context={'environment': 'test'})

        with self.assertRaises(Exception):
            ensure_scope(scope_id='app', scope_type='app', context={'environment': 'prod'})

    def test_cannot_add_to_context(self):
        ensure_scope(scope_id='app', scope_type='app', context={'environment': 'test'})

        with self.assertRaises(Exception):
            ensure_scope(scope_id='app', scope_type='app', context={'a': 'b'})

    def test_cannot_change_empty_context(self):
        ensure_scope(scope_id='app', scope_type='app')

        with self.assertRaises(Exception):
            ensure_scope(scope_id='app', scope_type='app', context={'a': 'b'})

    def test_cannot_change_context_in_child(self):
        ensure_scope(scope_id='app', scope_type='app', context={'environment': 'test'})

        with self.assertRaises(Exception):
            ensure_scope('child', scope_type='child', parent_id='app', context={'environment': 'prod'})

    def test_adding_context_to_child_scope_does_not_influence_root(self):
        ensure_scope(scope_id='child', scope_type='child', context={'environment': 'test'})

        root_resolver = get_resolver()

        with self.assertRaises(Exception):
            root_resolver(StringGenerator)

    def test_adding_context_to_child_scope_does_not_influence_root_dependencies(self):
        ensure_scope(scope_id='child', scope_type='child', context={'environment': 'test'})
        resolver = get_resolver('child')

        with self.assertRaises(Exception):
            resolver(str)

    def test_child_scope_inherits_parent_context(self):
        ensure_scope(scope_id='app', scope_type='app', context={'environment': 'test'})
        ensure_scope(scope_id='tenant-a', scope_type='tenant', parent_id='app')
        resolver = get_resolver('tenant-a')

        self.assertEqual('Hello', resolver(str))
