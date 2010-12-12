from lxml import etree

from amazonmp3.base import AmazonMetaclass
from amazonmp3.connection import AmazonMp3Connection


class AmazonQuery(object):
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

    def search(self, query, per_page=50, page_number=1,
               ordering='salesrank', match_criteria='field-keywords'):
        """Eagerly request a page of results.

        :param query: Amazon search query. *Required*
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
                      'type': self._meta.media_type.upper(),
                      'pagesize': per_page,
                      'page_number': page_number,
                      'sortby': ordering,
                      'matchcriteria': match_criteria}
        
        url = self.provider.build_url(**query_args)
        response = self.provider.make_request(url)
        return self.parse_response(response)
