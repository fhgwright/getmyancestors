"""OrderedSet implementation, based on OrderedDict."""

# Not worth copyrighting, by Frederick H. G. Wright II, 2020.

import collections


# Although some later Python implementations make the dict builtin an
# ordered dict, there isn't a well-defined way to test for this, so we
# use the OrderedDict import unconditionally.

#pylint: disable=too-many-ancestors
class OrderedSet(collections.OrderedDict, collections.MutableSet):
    """MutableSet with order preservation."""

    def __init__(self, *args, **kwargs):
        super(OrderedSet, self).__init__()
        self.__update(*args, **kwargs)

    def __update(self, *args, **kwargs):
        if kwargs:
            raise TypeError("__update() takes no keyword arguments")
        for arg in args:
            for val in arg:
                self.add(val)

    def add(self, value):
        self[value] = None

    def discard(self, value):
        self.pop(value, None)

    # Need to override __and__ to get expected ordering (order from self).
    # Version from MutableSet gets order from other.
    def __and__(self, other):
        if not isinstance(other, collections.Iterable):
            return NotImplemented
        others = set(other)
        return self.__class__([value for value in self if value in others])

    def __le__(self, other):
        return all(e in other for e in self)

    def __lt__(self, other):
        return self <= other and self != other

    def __ge__(self, other):
        return all(e in self for e in other)

    def __gt__(self, other):
        return self >= other and self != other

    def __repr__(self):
        return 'OrderedSet([%s])' % (', '.join(map(repr, self.keys())))

    def __str__(self):
        return '{%s}' % (', '.join(map(repr, self.keys())))

    difference = property(lambda self: self.__sub__)
    difference_update = property(lambda self: self.__isub__)
    intersection = property(lambda self: self.__and__)
    intersection_update = property(lambda self: self.__iand__)
    issubset = property(lambda self: self.__le__)
    issuperset = property(lambda self: self.__ge__)
    symmetric_difference = property(lambda self: self.__xor__)
    symmetric_difference_update = property(lambda self: self.__ixor__)
    union = property(lambda self: self.__or__)
