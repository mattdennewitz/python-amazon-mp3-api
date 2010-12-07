from amazonmp3.base import BaseModel
from amazonmp3.fields import *


class Track(BaseModel):
    """A single song.

    :param creator: Track's author/creator. Normally the primary artist.
    :param album: Album title
    :param title: Track title
    :param image: Default display image. Normally the cover artwork.
    :param duration: Track play time in milliseconds
    :param track_number: Track position on album
    :param asin: Track's Amazon Standard Identification Number
    :param album_asin: Album's Amazon Standard Identification Number
    :param audio_bitrate: MP3 bitrate
    :param filesize: MP3 filesize
    :param file_format: Track download file format
    :param thumbnail: Cover artwork thumbnail
    """
    creator = StringField()
    album = StringField()
    title = StringField()
    image = StringField()
    duration = IntegerField()
    track_number = IntegerField(api_path='trackNum')
    asin = StringField(api_path='.//meta[@rel="http://www.amazon.com/dmusic/ASIN"]')
    album_asin = StringField(api_path='.//meta[@rel="http://www.amazon.com/dmusic/albumASIN"]')
    audio_bitrate = IntegerField(api_path='.//meta[@rel="http://www.amazon.com/dmusic/audioBitrate"]')
    filesize = StringField(api_path='.//meta[@rel="http://www.amazon.com/dmusic/fileSize"]')
    file_format = StringField(api_path='.//meta[@rel="http://www.amazon.com/dmusic/fileFormat"]')
    thumbnail = StringField(api_path='.//meta[@rel="http://www.amazon.com/dmusic/imageThumb"]')
    
    def __repr__(self):
        return '[%s] %s - %s' % (self.asin, self.creator, self.title)

