# typedispatch

`typedispatch` is a Python library for registering functions based on type resolution. It allows you to associate types with functions and dynamically look up functions based on the type of an object, including handling inheritance hierarchies.

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

The library also provides a convenient decorator for registering functions with specific types. This makes the code cleaner and easier to manage.
```python
from typedispatch import TypeDispatch

typedispatch = TypeDispatch()

@typedispatch.register_decorator(int)
def handle_integer(x):
    return f"Handling integer: {x}"

@typedispatch.register_decorator(str)
def handle_string(x):
    return f"Handling string: {x}"

print(typedispatch.lookup(42))        # Output: Handling integer: 42
print(typedispatch.lookup("hello"))   # Output: Handling string: hello
```