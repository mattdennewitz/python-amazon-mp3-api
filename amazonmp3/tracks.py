from amazonmp3.base import BaseQuery, BaseModel
from amazonmp3 import fields


class Track(BaseModel):
    creator = fields.StringField()
    album = fields.StringField()
    title = fields.StringField()
    image = fields.StringField()
    duration = fields.IntegerField()
    track_number = fields.IntegerField(api_path='trackNum')
    asin = fields.StringField(api_path='.//meta[@rel="http://www.amazon.com/dmusic/albumASIN"]')

    def __repr__(self):
        return '[%s] %s - %s' % (self.asin, self.creator, self.title)

    
class TrackQuery(BaseQuery):

    class Meta:
        media_type = 'track'
        response_enclosure = 'track'
        object_class = Track


