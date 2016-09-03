__author__ = '__naresh__'


# check quantity instnces for more managed instances

# class Quantity:
#     def __init__(self, storage_name=None):
#         self.storage_name = storage_name

#     def __set__(self, instance, value):
#         if value > 0:
#             instance.__dict__[self.storage_name] = value
#         else:
#             raise ValueError('value must be > 0')

class Quantity(object):
    __counter = 0

    def __init__(self):
        """
        In init the storage name is '_Quantity#0' not '__quantity0'
        because name mangling of private variable is done when class 
        definition run.
        
        """
        cls = self.__class__
        prefix = cls.__name__
        self.storage_name = "_{0}#{1}".format(prefix, cls.__counter)
        cls.__counter += 1

    def __get__(self, instance, owner):
        return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        if value > 0:
            setattr(instance, self.storage_name, value)
        else:
            raise ValueError("Value must be greater than zero")


class LineItem(object):
    """
    Here weight, price is storage attribute

    _Quanitity#0, _Quantity#1 is a managed Attribute

    """
    weight = Quantity()
    price = Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


if __name__ == "__main__":
    l1 = LineItem("Apple", 10, 10)
    l2 = LineItem("Banana", 20, 20)
    l3 = LineItem("Grapes", 30, 30)
    l4 = LineItem("xyz", 40, 40)
    print(l1.weight)
    print(l2.weight)
    print(l3.weight)
    print(l4.weight)
