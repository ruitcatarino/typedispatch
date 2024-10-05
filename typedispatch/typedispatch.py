from collections import defaultdict


class TypeDispatchError(Exception):
    """Custom exception for errors related to TypeDispatch."""

    pass


class TypeDispatch:
    def __init__(self):
        self.registry = defaultdict(list)

    def register(self, obj_type, func, **predicate):
        """
        Register a type with a function.
        :param obj_type: The type (class) to be registered.
        :param func: The function to be associated with this type.
        """
        if not isinstance(obj_type, type):
            raise TypeDispatchError(f"{obj_type} is not a valid type.")

        self.registry[obj_type].append((predicate, func))

    def register_decorator(self, obj_type, **predicate):
        """
        Register a function as a decorator for the given type.
        :param obj_type: The type (class) to register the function with.
        :return: A decorator that registers the function for the given type.
        """

        def decorator(func):
            self.register(obj_type, func, **predicate)
            return func

        return decorator

    def lookup(self, obj, **predicate):
        """
        Find and execute the function associated with the object's type.
        This method will check the object's type and iterate over the MRO
        (method resolution order) to find the first match.

        :param obj: The object whose type will be checked.
        :return: The result of the function if found.
        :raises: TypeDispatchError if no function is found.
        """
        obj_type = type(obj)
        mro = obj_type.mro()

        for cls in mro:
            if cls in self.registry:
                for registered_predicate, func in self.registry[cls]:
                    if self._match_predicates(obj, predicate, registered_predicate):
                        return func(obj)
        raise TypeDispatchError(
            f"No function found for type {obj_type} or its superclasses."
        )

    def _match_predicates(self, obj, predicate, registered_predicate):
        """
        Check if all registered predicate match the given predicate.
        :param obj: The object being looked up.
        :param predicate: The object being looked up.
        :param registered_predicate: Dictionary of predicates to match.
        :return: True if predicate matches, False otherwise.
        """
        for registered_key, registered_value in registered_predicate.items():
            if (
                registered_key not in predicate
                or predicate.get(registered_key) != registered_value
            ):
                return False
        return True

    def is_registered(self, obj_type):
        """
        Check if a type or any of its superclasses is registered in the TypeDispatch.
        :param obj_type: The type (class) to check.
        :return: True if registered, False otherwise.
        """
        return obj_type in self.registry
