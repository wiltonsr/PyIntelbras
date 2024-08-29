class IntelbrasAPI:
    def __init__(self) -> None:
        pass

    def __getattr__(self, name):
        def method(*args, **kwargs):
            print(f"Call method '{
                  name}' with arguments: {args} and {kwargs}")
        return method
