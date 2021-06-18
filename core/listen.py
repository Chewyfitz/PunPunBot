from .engine import EventEngine

_e = EventEngine()

# Decorator-based subscription
def subscribe(name, **kwargs):
    # The wrapper function
    def _wrapper(func):
        # The wrapped function to be returned
        def __wrapped_function(*args, **kwargs):
            func(*args, **kwargs)
        # Subscribe the wrapped function
        subbed = _e.subscribe_to(func, name, **kwargs)
        if not subbed:
            print(f"Subscription of {func.__name__} to {name} failed!")
            print(f"{name}: {_e._EventEngine__engine.publishers[name]}")
        return __wrapped_function

    return _wrapper

