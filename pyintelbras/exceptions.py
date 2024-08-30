class IntelbrasAPIException(Exception):
    """Generic Intelbras API Exception"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self.error = kwargs.get("error", None)
