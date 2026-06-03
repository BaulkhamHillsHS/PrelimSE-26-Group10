from PIL import Image

#getting images
i_rom1 = Image.open("Images/Movies/Play_Movie/Romance1.png")
i_rom2 = Image.open("Images/Movies/Play_Movie/Romance2.png")
i_rom3 = Image.open("Images/Movies/Play_Movie/Romance3.png")
i_rom4 = Image.open("Images/Movies/Play_Movie/Romance4.png")
i_hor1 = Image.open("Images/Movies/Play_Movie/Horror1.png")
i_hor2 = Image.open("Images/Movies/Play_Movie/Horror2.png")
i_hor3 = Image.open("Images/Movies/Play_Movie/Horror3.png")
i_hor4 = Image.open("Images/Movies/Play_Movie/Horror4.png")
i_act1 = Image.open("Images/Movies/Play_Movie/Action1.png")
i_act2 = Image.open("Images/Movies/Play_Movie/Action2.png")
i_act3 = Image.open("Images/Movies/Play_Movie/Action3.png")
i_act4 = Image.open("Images/Movies/Play_Movie/Action4.png")

# classes and functions related to videos 
# e.g. filtering
class VideoData:
    """
    Base class for tv shows and movies
    """
    def __init__(self, name, age_rating, genres, filters, thumbnail, video):
        self.name = name
        self.age_rating = age_rating
        self.genres = genres
        self.filters = filters
        self.thumbnail = thumbnail
        self.video = video
        
        #prevents someone from accidentily setting an age rating that is not included in the filters
        accepted_age_ratings = {"G","PG","M","MA15+","R"}
        if age_rating not in accepted_age_ratings:
            raise Exception(age_rating + " is not an accepted age rating")

class MovieData(VideoData):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
                        

class TVShowData(VideoData):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

#Creating movie list to import into main.py
m_rom1 = MovieData("rom1","PG", "Romance", "Family Movie", i_rom1, i_rom1)
m_rom2 = MovieData("rom2","M", "Romance", "Oscar Nominee", i_rom2, i_rom2)
m_rom3 = MovieData("rom3","G", "Romance", "Family Movie", i_rom3, i_rom3)
m_rom4 = MovieData("rom4","PG", "Romance", "Family Movie", i_rom4, i_rom4)



movies = [m_rom1,m_rom2,m_rom3,m_rom4]