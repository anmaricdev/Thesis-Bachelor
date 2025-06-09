class Item:
    def __init__(self, size):
        self.size = size
        self._color = None
        self.is_packed_after_failure = False

    def __repr__(self):
        return f"Item({self.size})"

    # Override addition operator
    def __add__(self, other):
        if isinstance(other, Item):
            return self.size + other.size
        else:
            return self.size + other

    # Override subtraction operator
    def __sub__(self, other):
        if isinstance(other, Item):
            return self.size - other.size
        else:
            return self.size - other

    # Override addition operator when item is the right operand
    def __radd__(self, other):
        return self.__add__(other)

    # Override subtraction operator when item is the right operand
    def __rsub__(self, other):
        if isinstance(other, Item):
            return other.size - self.size
        else:
            return other - self.size


def create_items_bulk(*items):
    return list(map(lambda item: Item(item), items))


def fixed_capacity(capacity, amount_bins):
    return [capacity] * amount_bins