from amazonmp3.connection import AmazonMp3Connection


class QueryOptionSet(object):
    media_type = None
    response_enclosure = None
    object_class = None

    def __new__(cls, meta=None):
        overrides = {}
        if meta is not None:
            for key in dir(meta):
                if key.startswith('_'):
                    continue
                value = getattr(meta, key)
                overrides[key] = value
            return object.__new__(type('QueryOptionSet',
                                       (cls, ),
                                       overrides))


class AmazonMetaclass(type):

    def __new__(cls, name, bases, attrs):
        new_cls = super(AmazonMetaclass, cls).__new__(cls, name, bases,
                                                      attrs)
        if '__metaclass__' in attrs:
            return new_cls

        meta_opts = getattr(new_cls, 'Meta', None)
        new_cls._meta = QueryOptionSet(meta_opts)

        return new_cls


class AmazonModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        new_cls = super(AmazonModelMetaclass, cls).__new__(cls, name, bases, 
                                                           attrs)

        if attrs.get('__metaclass__') == AmazonModelMetaclass:
            return new_cls
        
        fields = {}

        for key, value in attrs.iteritems():
            if isinstance(value, BaseField):
                value.field_name = key
                if value.api_path is None:
                    value.api_path = key
                fields[key] = value
        
        new_cls._fields = fields

        return new_cls


class BaseField(object):

    def __init__(self, field_name=None, api_path=None, default=None,
                 converter=None):
        self.field_name = field_name
        self.api_path = api_path
        self.default = default

    def __get__(self, instance, owner):
        value = instance._data.get(self.field_name)
        if value is None:
            return self.default
        return value

    def __set__(self, instance, value):
        instance._data[self.field_name] = value

        
class BaseModel(object):
    __metaclass__ = AmazonModelMetaclass

    def __init__(self, **values):
        self._data = {}

        for field_name in self._fields.keys():
            try:
                setattr(self, field_name, values.pop(field_name))
            except AttributeError:
                pass

    @classmethod
    def _from_xml(cls, node):
        values = {}

        for field_name, field in cls._fields.items():
            value = None
            value_node = node.find(field.api_path)
            if value_node is not None:
                value = value_node.text
            if value is not None:
                value = field.to_python(value)
            values[field_name] = value

        return cls(**values)
            

