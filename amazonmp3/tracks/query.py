from amazonmp3.query import AmazonQuery
from amazonmp3.tracks.models import Track


class TrackQuery(AmazonQuery):

    class Meta:
        media_type = 'track'
        response_enclosure = 'track'
        object_class = Track


