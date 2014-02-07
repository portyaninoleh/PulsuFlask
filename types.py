class BaseType(object):
    def get_value(self):
        raise NotImplementedError()


class EmptyStringType(BaseType):
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value


class StringType(BaseType):
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value


class ExpressionType(BaseType):
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value


class IntType(BaseType):
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value


class TypeFactory(object):
    # Types fabric
    object={
        'empty_string': EmptyStringType,
        'string': StringType,
        'expression': ExpressionType,
        'int': IntType
    }

    def get_type(self, name='default', value=''):
        return self.object[name](value)

factory = TypeFactory()