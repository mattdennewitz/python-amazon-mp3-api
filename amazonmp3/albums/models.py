from amazonmp3.base import BaseModel
from amazonmp3.fields import *


class Album(BaseModel):
    """A single album.

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
    asin = StringField(api_path='.//meta[@rel="http://www.amazon.com/dmusic/ASIN"]')
    product_type = StringField(api_path='.//meta[@rel="http://www.amazon.com/dmusic/productTypeName"]')
    primary_genre = StringField(api_path='../meta[@rel="http://www.amazon.com/dmusic/primaryGenre"]')
    label = StringField(api_path='.//meta[@rel="http://www.amazon.com/dmusic/label"]')
    average_overall_rating = StringField(api_path='.//meta[@rel="http://www.amazon.com/dmusic/averageOverallRating"]')
    artist_asin = StringField(api_path='.//meta[@rel="http://www.amazon.com/dmusic/artistASIN"]')
    tiny_image = StringField(api_path='.//meta[@rel="http://www.amazon.com/dmusic/imageTiny"]')
    thumbnail_image = StringField(api_path='.//meta[@rel="http://www.amazon.com/dmusic/imageThumb"]')
    medium_image = StringField(api_path='.//meta[@rel="http://www.amazon.com/dmusic/imageMedium"]')
    large_image = StringField(api_path='.//meta[@rel="http://www.amazon.com/dmusic/imageLarge"]')
    delivery_restrictions = StringField(api_path='.//meta[@rel="http://www.amazon.com/dmusic/deliveryRestrictions"]')
    release_date = DateField(api_path='.//meta[@rel="http://www.amazon.com/dmusic/releaseDate"]',
                             format='%Y%m%d')
    original_release_date = DateField(api_path='.//meta[@rel="http://www.amazon.com/dmusic/originalReleaseDate"]',
                                      format='%Y%m%d')
    street_date = DateField(api_path='.//meta[@rel="http://www.amazon.com/dmusic/streetDate"]',
                            format='%Y%m%d')
    seller = StringField(api_path='.//meta[@rel="http://www.amazon.com/dmusic/seller"]')    
    dmid = StringField(api_path='.//meta[@rel="http://www.amazon.com/dmusic/DMID"]')
    price = StringField(api_path='.//meta[@rel="http://www.amazon.com/dmusic/price"]')

    def __repr__(self):
        return '[%s] %s - %s' % (self.asin, self.creator, self.title)

