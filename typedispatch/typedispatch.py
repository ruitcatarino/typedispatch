from collections import defaultdict
from typing import Callable, Type, Any, Dict, List, Tuple
from functools import wraps


class TypeDispatchError(Exception):
    """Custom exception for errors related to TypeDispatch."""

    pass


class TypeDispatch:
    def __init__(self):
        self.registry: Dict[Type, List[Tuple[Dict[str, Any], Callable]]] = defaultdict(
            list
        )

    def register(self, obj_type: Type, func: Callable, **predicate: Any) -> None:
        """
        Register a type with a function.
        :param obj_type: The type (class) to be registered.
        :param func: The function to be associated with this type.
        """
        if not isinstance(obj_type, type):
            raise TypeDispatchError(f"{obj_type} is not a valid type.")

        self.registry[obj_type].append((predicate, func))

    def register_decorator(self, obj_type: Type, **predicate: Any) -> Callable:
        """
        Register a function as a decorator for the given type.
        :param obj_type: The type (class) to register the function with.
        :param predicate: Optional predicates to match when dispatching.
        :return: A decorator that registers the function for the given type.
        """

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapped_func(*args, **kwargs):
                return func(*args, **kwargs)

            self.register(obj_type, func, **predicate)
            return wrapped_func

        return decorator

    def lookup(self, obj: Any, **predicate: Any) -> Any:
        """
        Find and execute the function associated with the object's type.
        This method will check the object's type and iterate over the MRO
        (method resolution order) to find the first match.

        :param obj: The object whose type will be checked.
        :return: The result of the function if found.
        :raises: TypeDispatchError if no function is found.
        """
        obj_type = type(obj)

        for cls in obj_type.mro():
            if cls in self.registry:
                for registered_predicate, func in self.registry[cls]:
                    if self._match_predicates(predicate, registered_predicate):
                        return func(obj)
        raise TypeDispatchError(
            f"No function found for type {obj_type} or its superclasses."
        )

    def _match_predicates(
        self, predicate: Dict[str, Any], registered_predicate: Dict[str, Any]
    ) -> bool:
        """
        Check if all registered predicate match the given predicate.
        :param obj: The object being looked up.
        :param predicate: The object being looked up.
        :param registered_predicate: Dictionary of predicates to match.
        :return: True if predicate matches, False otherwise.
        """
        return all(
            key in predicate and predicate.get(key) == value
            for key, value in registered_predicate.items()
        )

    def is_registered(self, obj_type: Type) -> bool:
        """
        Check if a type or any of its superclasses is registered in the TypeDispatch.
        :param obj_type: The type (class) to check.
        :return: True if registered, False otherwise.
        """
        return obj_type in self.registry
