class Selected:
    def __init__(self):
        self.object = None

    def set_selected(self, obj):
        self.object = obj

    def get_selected(self):
        return self.object
    
    def clear(self):
        self.object = None

    def is_clear(self):
        return self.object is None
