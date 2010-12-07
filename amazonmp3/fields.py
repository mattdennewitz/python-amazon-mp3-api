from amazonmp3.base import BaseField


__all__ = ['StringField', 'IntegerField', 'ObjectField',
           'ListField', 'Field']


class Field(BaseField):
    
    def to_python(self, value):
        return value


class StringField(Field):
    
    def to_python(self, value):
        return value.encode('utf-8')


class IntegerField(Field):

    def to_python(self, value):
        return int(value)


class ObjectField(Field):

    def __init__(self, object_cls, **kwargs):
        self.object_cls = object_cls
        ObjectField.__init__(self, **kwargs)

    def to_python(self, value):
        return self.object_cls._from_xml(value)


class ListField(Field):

    def __init__(self, field=None, **kwargs):
        self.field = field
        ListField.__init__(self, **kwargs)

    def to_python(self, values):
        def iterate_values(values):
            for value in values:
                yield self.field.to_python(value)

        if self.field is None:
            return values

        return iterate_values(values)


