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

        self.assertEqual(
            self.typedispatch.lookup(MyList([1, 2, 3])), "List of length 3"
        )

    def test_no_function_found(self):
        with self.assertRaises(TypeDispatchError):
            self.typedispatch.lookup(3.14)

    def test_is_registered(self):
        self.typedispatch.register(str, lambda x: f"String {x}")
        self.assertTrue(self.typedispatch.is_registered(str))

        self.assertFalse(self.typedispatch.is_registered(float))

    def test_register_decorator(self):
        @self.typedispatch.register_decorator(int)
        def handle_int(x):
            return f"Handling integer {x}"

        self.assertEqual(self.typedispatch.lookup(10), "Handling integer 10")

    def test_register_invalid_type(self):
        with self.assertRaises(TypeDispatchError):
            self.typedispatch.register("not_a_type", lambda x: x)

    def test_register_multiple_types(self):
        self.typedispatch.register(int, lambda x: f"Integer {x}")
        self.typedispatch.register(str, lambda x: f"String {x}")
        self.assertEqual(self.typedispatch.lookup(99), "Integer 99")
        self.assertEqual(self.typedispatch.lookup("hello"), "String hello")

    def test_multiple_inheritance_lookup(self):
        class A:
            pass

        class B(A):
            pass

        class C(B):
            pass

        self.typedispatch.register(A, lambda x: "Handling A")
        self.typedispatch.register(B, lambda x: "Handling B")

        self.assertEqual(self.typedispatch.lookup(C()), "Handling B")
        del self.typedispatch.registry[B]
        self.assertEqual(self.typedispatch.lookup(C()), "Handling A")

    def test_decorator_inheritance(self):
        @self.typedispatch.register_decorator(float)
        def handle_float(x):
            return f"Handling float {x}"

        class MyFloat(float):
            pass

        self.assertEqual(self.typedispatch.lookup(MyFloat(1.23)), "Handling float 1.23")


if __name__ == "__main__":
    unittest.main()
