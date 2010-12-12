from amazonmp3.query import AmazonQuery
from amazonmp3.albums.models import Album


class AlbumQuery(AmazonQuery):

    class Meta:
        media_type = 'album'
        response_enclosure = 'album'
        object_class = Album


