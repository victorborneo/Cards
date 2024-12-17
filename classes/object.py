class MissingMethodError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Object:
    def draw(self, *args, **kwargs):
        raise MissingMethodError(f"Class '{self.__class__.__name__}' missing method 'draw'")

    def update(self, *args, **kwargs):
        raise MissingMethodError(f"Class '{self.__class__.__name__}' missing method 'update'")
    
    def clicked(self, *args, **kwargs):
        raise MissingMethodError(f"Class '{self.__class__.__name__}' missing method 'clicked'")
    
    def on_click(self, *args, **kwargs):
        raise MissingMethodError(f"Class '{self.__class__.__name__}' missing method 'on_click'")
