class Item:
    def __init__(self, size):
        self.size = size
        self._color = None  # This will be set by the visualization
    
    def __add__(self, other):
        if isinstance(other, Item):
            return self.size + other.size
        return self.size + other
    
    def __radd__(self, other):
        return self.__add__(other)

def create_items_bulk(*sizes):
    return [Item(size) for size in sizes] 