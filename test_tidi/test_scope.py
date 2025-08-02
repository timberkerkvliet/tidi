from unittest import TestCase
from test_tidi import scope_composition

from test_tidi.scope_composition import Animal, Hey, User

from tidi import scan, get_scope, clear_scope, clear_all_scopes


class TestResolver(TestCase):
    def setUp(self) -> None:
        scan(scope_composition)
        self.resolver = get_scope()

    def tearDown(self) -> None:
        clear_all_scopes()

    def test_no_singleton(self):
        with self.assertRaises(Exception):
            self.resolver(Animal)

    def test_cannot_get_root_scope_with_other_scope(self):
        with self.assertRaises(Exception):
            get_scope(scope_id='root', scope_type='transient')

    def test_cannot_get_root_scope_with_parent(self):
        with self.assertRaises(Exception):
            get_scope(scope_id='root', parent_id='other')

    def test_create_scope(self):
        resolver = get_scope(scope_id='tenant-a', scope_type='tenant')
        result = resolver(Animal)

        self.assertEqual(Animal(name='Henk'), result)

    def test_ensure_scope(self):
        resolver = get_scope(scope_id='tenant-a', scope_type='tenant')
        result = resolver(Animal)

        self.assertEqual(Animal(name='Henk'), result)

    def test_ensure_twice(self):
        get_scope(scope_id='tenant-a', scope_type='tenant')

        resolver = get_scope(scope_id='tenant-a', scope_type='tenant')
        result = resolver(Animal)

        self.assertEqual(Animal(name='Henk'), result)

    def test_ensure_with_other_type(self):
        get_scope(scope_id='tenant-a', scope_type='tenant')

        with self.assertRaises(Exception):
            get_scope(scope_id='tenant-a', scope_type='iets')

    def test_destroy_scope(self):
        get_scope(scope_id='tenant-a', scope_type='tenant')
        clear_scope(scope_id='tenant-a')

        with self.assertRaises(Exception):
            get_scope('tenant-a')

    def test_can_access_root_scope(self):
        resolver = get_scope(scope_id='tenant-a', scope_type='tenant')

        result = resolver(Hey)

        self.assertEqual(Hey(age=17), result)

    def test_nested_scopes(self):
        get_scope(scope_id='tenant-a', scope_type='tenant')
        resolver = get_scope(scope_id='request-b', scope_type='request', parent_id='tenant-a')

        user_result = resolver(User)
        hey_result = resolver(Hey)

        self.assertEqual(User(id='user'), user_result)
        self.assertEqual(Hey(age=17), hey_result)

    def test_cannot_nest_same_type(self):
        get_scope(scope_id='tenant-a', scope_type='tenant')

        with self.assertRaises(Exception):
            get_scope(scope_id='tenant-b', scope_type='tenant', parent_id='tenant-a')
