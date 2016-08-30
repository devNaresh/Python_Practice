__author__ = '__naresh__'

from collections import abc
import requests

URL = 'http://www.oreilly.com/pub/sc/osconfeed'


class FrozenJSON:
    """A read-only façade for navigating a JSON-like object
    using attribute notation
    """
    def __new__(cls, arg):
        if isinstance(arg, abc.Mapping):
            return super().__new__(cls)
        elif isinstance(arg, abc.MutableSequence):
            return [cls(item) for item in arg]
        else:
            return arg

    def __init__(self, mapping):
        self.__data = dict(mapping)

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return FrozenJSON(self.__data[name])

    # @classmethod
    # def build(cls, obj):
    #     if isinstance(obj, abc.Mapping):
    #         return cls(obj)
    #     elif isinstance(obj, abc.MutableSequence):
    #         return [cls.build(item) for item in obj]
    #     else:
    #         return obj


def get_data():
    data = requests.get(URL).json()
    data = FrozenJSON(data)
    return data


if __name__ == "__main__":
    feed = get_data()
    print(len(feed.Schedule.speakers))
    print(sorted(feed.Schedule.keys()))
    print(feed.Schedule.speakers[-1].name)
    talk = feed.Schedule.events[40]
    print(type(talk))
    print(talk.name)
    print(talk.speakers)
    #print(talk.flavour)
