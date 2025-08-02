from unittest import TestCase
from test_tidi import scope_composition

from test_tidi.scope_composition import Animal, Hey, User

from tidi import scan, get_resolver, create_scope, ensure_scope, destroy_scope, destroy_all


class TestResolver(TestCase):
    def setUp(self) -> None:
        scan(scope_composition)
        self.resolver = get_resolver()

    def tearDown(self) -> None:
        destroy_all()

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

    def test_can_access_root_scope(self):
        ensure_scope(scope_id='tenant-a', scope_type='tenant')

        resolver = get_resolver('tenant-a')

        result = resolver(Hey)

        self.assertEqual(Hey(age=17), result)

    def test_nested_scopes(self):
        ensure_scope(scope_id='tenant-a', scope_type='tenant')
        ensure_scope(scope_id='request-b', scope_type='request', parent_id='tenant-a')

        resolver = get_resolver('request-b')

        user_result = resolver(User)
        hey_result = resolver(Hey)

        self.assertEqual(User(id='user'), user_result)
        self.assertEqual(Hey(age=17), hey_result)

    def test_cannot_nest_same_type(self):
        ensure_scope(scope_id='tenant-a', scope_type='tenant')

        with self.assertRaises(Exception):
            ensure_scope(scope_id='tenant-b', scope_type='tenant', parent_id='tenant-a')
