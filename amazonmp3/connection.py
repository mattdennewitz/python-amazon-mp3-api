import urllib
import urlparse

import httplib2

from lxml import etree


class AmazonMp3Connection(object):

    SearchApiUrl = 'http://www.amazon.com/gp/dmusic/aws/search.html'

    def __init__(self):
        self.connection = httplib2.Http('.amazon_mp3_api')

    def make_request(self, url, method='GET', body=None, headers=None):
        """Make an HTTP request.
        """

        headers = headers or {}
        body = body or {}

        # make request
        response, content = self.connection.request(url, method, body, 
                                                    headers)

        # handle response
        # FIXME: this is awfully naive
        if int(response.status) > 400:
            raise SongkickRequestError('Could not load %s: [%s] %s' % \
                                       (url, response.status,
                                        response.reason))
        return content

    def build_url(self, **request_args):
        "Build Amazon URL"

        # break down the url into its components, inject args
        # as query string and recombine the url
        url_parts = list(urlparse.urlparse(AmazonMp3Connection.SearchApiUrl))
        url_parts[4] = urllib.urlencode(request_args)
        url = urlparse.urlunparse(url_parts)
        
        return url

    



