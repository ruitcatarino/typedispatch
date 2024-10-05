# typedispatch

`typedispatch` is a Python library for registering functions based on type resolution. It allows you to associate types with functions and dynamically look up functions based on the type of an object, including handling inheritance hierarchies.

## Installation

```bash
pip install typedispatch
```

## Usage
```python
from typedispatch import TypeDispatch, TypeDispatchError

typedispatch = TypeDispatch()

typedispatch.register(int, lambda x: f"Processing integer: {x}")
print(typedispatch.lookup(10))  # Output: Processing integer: 10
```
