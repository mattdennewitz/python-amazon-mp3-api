from amazonmp3.base import BaseQuery, BaseModel
from amazonmp3 import fields


class Track(BaseModel):
    creator = fields.StringField()
    album = fields.StringField()
    title = fields.StringField()
    image = fields.StringField()
    duration = fields.IntegerField()
    track_number = fields.IntegerField(api_path='trackNum')

    def __repr__(self):
        return '%s - %s [%s]' % (self.creator, self.title, self.album)

    
class TrackQuery(BaseQuery):

    class Meta:
        media_type = 'track'
        response_enclosure = 'track'
        object_class = Track


