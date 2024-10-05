class TypeDispatchError(Exception):
    """Custom exception for errors related to TypeDispatch."""

    pass


class TypeDispatch:
    def __init__(self):
        self.registry = {}

    def register(self, obj_type, func):
        """
        Register a type with a function.
        :param obj_type: The type (class) to be registered.
        :param func: The function to be associated with this type.
        """
        if not isinstance(obj_type, type):
            raise TypeDispatchError(f"{obj_type} is not a valid type.")

        self.registry[obj_type] = func

    def register_decorator(self, obj_type):
        """
        Register a function as a decorator for the given type.
        :param obj_type: The type (class) to register the function with.
        :return: A decorator that registers the function for the given type.
        """

        def decorator(func):
            self.register(obj_type, func)
            return func

        return decorator

    def lookup(self, obj):
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
                return self.registry[cls](obj)
        raise TypeDispatchError(
            f"No function found for type {obj_type} or its superclasses."
        )

    def is_registered(self, obj_type):
        """
        Check if a type or any of its superclasses is registered in the TypeDispatch.
        :param obj_type: The type (class) to check.
        :return: True if registered, False otherwise.
        """
        return obj_type in self.registry
