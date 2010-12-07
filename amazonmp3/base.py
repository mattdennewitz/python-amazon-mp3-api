from lxml import etree

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


class AmazonModelMetaclass(AmazonMetaclass):

    def __new__(cls, name, bases, attrs):
        # super_new = super(AmazonModelMetaclass, cls).__new__
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

    def __init__(self, field_name=None, api_path=None, default=None):
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


class BaseQuery(object):
    __metaclass__ = AmazonMetaclass

    def __init__(self, client_id):
        self.client_id = client_id
        self.provider = AmazonMp3Connection()        

    @classmethod
    def parse_response(cls, response):
        """Parse XML results from Amazon search.
        """

        try:
            response_doc = etree.fromstring(response)
        except Exception, exc:
            raise Exception('Parsing response failed: %s' % exc)

        path = '//results/result/' + cls._meta.response_enclosure
        result_set = response_doc.xpath(path)

        for node in result_set:
            yield cls._meta.object_class._from_xml(node)

    def search(self, query, media_type='track', per_page=50, page_number=1,
               ordering='salesrank', match_criteria='field-keywords'):
        """Eagerly request a page of results.

        :param query: Amazon search query. *Required*
        :param media_type: Media type constraint. 
                           One of "track", "album" or "artist".
                           Default is "track". *Required*
        :param per_page: Objects per page. Default (and max) is 50.
        :param page_number: Result set page number. Default is 1.
        :param ordering: Optional sort parameter. Default is 'salesrank'.
        :param match_criteria: Optionally ask for results to match keywords, title, 
                               and/or author. Default is 'keywords'.

        .. todo:: Implement 'genrenode'. Remember, 'genrenode' 
                  doesn't work for ARTIST type.
        """

        # translate clean args into what amazon expects
        query_args = {'clientid': self.client_id,
                      'field-keywords': query,
                      'type': media_type.upper(),
                      'pagesize': per_page,
                      'page_number': page_number,
                      'sortby': ordering,
                      'matchcriteria': match_criteria}
        
        url = self.provider.build_url(**query_args)
        response = self.provider.make_request(url)
        return self.parse_response(response)

        
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
            

