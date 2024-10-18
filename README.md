# typedispatch

`typedispatch` is a Python library that provides a flexible and powerful mechanism for registering functions based on type resolution. It allows you to associate types with functions and dynamically look up functions based on the type of an object, including handling inheritance hierarchies and predicate-based dispatch.

## Features

- Register functions for specific types
- Automatic type resolution based on inheritance
- Decorator syntax for easy registration
- Predicate-based function dispatch
- Supports multiple inheritance

## Installation

```bash
pip install typedispatch
```

## Usage

### Basic Registration

You can register functions directly with the `register` method:

```python
from typedispatch import TypeDispatch, TypeDispatchError

typedispatch = TypeDispatch()
typedispatch.register(int, lambda x: f"Processing integer: {x}")

print(typedispatch.lookup(10))  # Output: Processing integer: 10
```

### Using the Decorator

The library provides a convenient decorator for registering functions with specific types:

```python
from typedispatch import TypeDispatch

typedispatch = TypeDispatch()

@typedispatch.register(int)
def handle_integer(x):
    return f"Handling integer: {x}"

@typedispatch.register(str)
def handle_string(x):
    return f"Handling string: {x}"

print(typedispatch.lookup(42))        # Output: Handling integer: 42
print(typedispatch.lookup("hello"))   # Output: Handling string: hello
```

### Inheritance-based Dispatch

It automatically handles inheritance hierarchies:

```python
typedispatch.register(list, lambda x: f"List of length {len(x)}")

class MyList(list):
    pass

print(typedispatch.lookup(MyList([1, 2, 3])))  # Output: List of length 3
```

### Predicate-based Dispatch

You can use predicates to further refine the dispatch logic:

```python
@typedispatch.register(int, a=True)
def handle_a_ints(x):
    return f"A integer {x}"

@typedispatch.register(int, b=True)
def handle_b_ints(x):
    return f"B integer {x}"

class MyInt(int):
    pass

@typedispatch.register(MyInt, a=True)
def handle_a_myints(x):
    return f"A MyInt {x}"

print(typedispatch.lookup(2, a=True))          # Output: A integer 2
print(typedispatch.lookup(2, b=True))          # Output: B integer 2
print(typedispatch.lookup(MyInt(2), a=True))   # Output: A MyInt 2
print(typedispatch.lookup(MyInt(2), b=True))   # Output: B integer 2
```

### Error Handling

When no matching function is found, a `TypeDispatchError` is raised:

```python
try:
    typedispatch.lookup(3.14)  # Assuming no function registered for float
except TypeDispatchError as e:
    print(f"Error: {e}")  # Output: Error: No function found for type <class 'float'> or its superclasses.
```

## API Reference

### `TypeDispatch`

- `register(obj_type: Type, func: Callable = None, **predicate: Any) -> Callable`: Register a function for a specific type. If called with a function, it registers it immediately; if called with only a type, it returns a decorator for registering functions.

- `lookup(obj: Any, **predicate: Dict[str, Any]) -> Any`: Find and execute the function associated with the object's type and optional predicates.

- `is_registered(obj_type: Type) -> bool`: Check if a type or any of its superclasses is registered in the TypeDispatch.

### Exceptions

- `TypeDispatchError`: Raised when no matching function is found or when an invalid type is registered.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).