class BaseType(object):
    @property
    def get_value(self):
        raise NotImplementedError()


class EmptyStringType(BaseType):
    def __init__(self, value):
        self.value = value

    @property
    def get_value(self):
        return self.value


class StringType(BaseType):
    def __init__(self, value):
        self.value = value

    @property
    def get_value(self):
        return self.value


class ExpressionType(BaseType):
    def __init__(self, value):
        self.value = value

    @property
    def get_value(self):
        return self.value


class IntType(BaseType):
    def __init__(self, value):
        self.value = value

    @property
    def get_value(self):
        return self.value


class ErrorType(BaseType):
    def __init__(self, value):
        self.value = value

    @property
    def get_value(self):
        return self.value


class TypeFactory(object):
    # Types fabric
    object={
        'empty_string': EmptyStringType,
        'string': StringType,
        'expression': ExpressionType,
        'int': IntType,
        'error': ErrorType
    }

    def get_type(self, name='default', value=u''):
        return self.object[name](value)

factory = TypeFactory()