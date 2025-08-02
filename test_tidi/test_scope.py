from unittest import TestCase
from test_tidi import composition_root
from test_tidi.composition_root.scopes import Animal

from tidi import scan, get_resolver, create_scope, ensure_scope, destroy_scope


class TestResolver(TestCase):
    def setUp(self) -> None:
        scan(composition_root)
        self.resolver = get_resolver()

    def test_no_singleton(self):
        with self.assertRaises(Exception):
            self.resolver(Animal)

    def test_create_scope(self):
        create_scope(scope_id='tenant-a', scope_type='tenant')
        resolver = get_resolver('tenant-a')
        result = resolver(Animal)

        self.assertEqual(Animal(name='Henk'), result)

    def test_ensure_scope(self):
        ensure_scope(scope_id='tenant-a', scope_type='tenant')
        resolver = get_resolver('tenant-a')
        result = resolver(Animal)

        self.assertEqual(Animal(name='Henk'), result)

    def test_ensure_twice(self):
        ensure_scope(scope_id='tenant-a', scope_type='tenant')
        ensure_scope(scope_id='tenant-a', scope_type='tenant')
        resolver = get_resolver('tenant-a')
        result = resolver(Animal)

        self.assertEqual(Animal(name='Henk'), result)

    def test_ensure_with_other_type(self):
        ensure_scope(scope_id='tenant-a', scope_type='tenant')

        with self.assertRaises(Exception):
            ensure_scope(scope_id='tenant-a', scope_type='iets')

    def test_destroy_scope(self):
        ensure_scope(scope_id='tenant-a', scope_type='tenant')
        destroy_scope(scope_id='tenant-a')

        with self.assertRaises(Exception):
            get_resolver('tenant-a')
