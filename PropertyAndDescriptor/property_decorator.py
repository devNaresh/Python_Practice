__author__ = '__naresh__'


class LineItem:
    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value):
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('value must be > 0')

    #weight = property(get_weight, set_weight)


def quantity(storage_name):
    def qty_getter(instance):
        return instance.__dict__[storage_name]

    def qty_setter(instance, value):
        if value > 0:
            instance.__dict__[storage_name] = value
        else:
            raise ValueError('value must be > 0')

    return property(qty_getter, qty_setter)


class LineItemFactory:
    weight = quantity('weight')
    price = quantity('price')

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


class Meta(type):
    def __getattribute__(*args):
        print("Metaclass getattribute invoked")
        return type.__getattribute__(*args)


class C(object, metaclass=Meta):
    def __len__(self):
        return 10

    def __getattribute__(*args):
        print("Class getattribute invoked")
        return object.__getattribute__(*args)


if __name__ == "__main__":
    l1 = LineItem("Apple", 10, 10)
    l1.weight
    # # l1 = LineItemFactory("Apple", 10, 10)
    # # l1.weight
    #
    # c = C()
    # c.__len__()  # Explicit lookup via instance
    #
    # type(c).__len__(c)  # Explicit lookup via type
    #
    # len(c)  # Implicit lookup
