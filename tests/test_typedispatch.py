import unittest
from typedispatch import TypeDispatch, TypeDispatchError

class TestTypeDispatch(unittest.TestCase):
    def setUp(self):
        self.typedispatch = TypeDispatch()

    def test_register_and_lookup(self):
        self.typedispatch.register(int, lambda x: f"Integer {x}")
        self.assertEqual(self.typedispatch.lookup(42), "Integer 42")

    def test_lookup_inheritance(self):
        self.typedispatch.register(list, lambda x: f"List of length {len(x)}")
        class MyList(list):
            pass
        self.assertEqual(self.typedispatch.lookup(MyList([1, 2, 3])), "List of length 3")

    def test_no_function_found(self):
        with self.assertRaises(TypeDispatchError):
            self.typedispatch.lookup(3.14)

if __name__ == '__main__':
    unittest.main()