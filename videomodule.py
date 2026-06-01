# classes and functions related to videos 
# e.g. filtering

class VideoData:
    """
    Base class for tv shows and movies
    """
    def __init__(self, name, age_rating, genres, filters, thumbnail):
        self.name = name
        self.age_rating = age_rating
        self.genres = genres
        self.filters = filters
        self.thumbnail = thumbnail

class MovieData(VideoData):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class TvShowData(VideoData):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)