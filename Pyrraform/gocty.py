import abc

# This is a partial Python implementation of
# https://github.com/zclconf/go-cty/blob/4e1b2a3ccc87ef459dac0e425f139c117a2d790f/cty/json.go#L16


class Type(abc.ABC):
    @abc.abstractmethod
    def to_data(self):
        pass


class Primitive(Type):
    def __init__(self, data):
        self.__data = data

    def to_data(self):
        return self.__data


Number = Primitive("number")
String = Primitive("string")
Boolean = Primitive("bool")


class List(Type):
    def __init__(self, element):
        self.__element = element

    def to_data(self):
        return ["list", self.__element.to_data()]


class Object(Type):
    def __init__(self, **properties):
        self.__properties = properties

    def to_data(self):
        return ["object", {k:v.to_data() for k, v in self.__properties.items()}]
