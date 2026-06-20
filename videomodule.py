from PIL import Image
from PIL import UnidentifiedImageError
import csvmodule as csvMod
import requests
from io import BytesIO

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
    AgeRatings = {"G": 0,"PG": 0,"M" : 12,"MA15+": 15,"R": 18}
    def __init__(self, id, title, backdrop_path="", age_rating="", genre_ids=[], **kwargs):
        self.ID = id
        self.name = title
        self.backdroppath = backdrop_path
        self.backdropimage = None
        self.age_rating = age_rating
        self.genres = genre_ids.replace("]", "").replace("[", "").split(", ")
        self.loaded = (id and title and backdrop_path and age_rating and genre_ids) or False
    
    def loadGenres(self): #convert numbers to genres
        pass
    
    def loadImage(self, *args): # method to override
        print("override this method in class ", type(self).__name__)
    
    def load(self): # method to override
        pass

class MovieData(VideoData):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def loadImage(self, path):
        if path:
            try:
                ImageURL = "https://image.tmdb.org/t/p/w200" + path
                response = requests.get(ImageURL)
                information = BytesIO(response.content)
                return Image.open(information)
            except UnidentifiedImageError:
                print("path", path, "could not be found")
    
    def loadImages(self):
        if self.loaded:
            self.backdropimage = self.loadImage(self.backdroppath)
    
    def load(self):
        if not self.loaded:
            #fields are id,title,backdrop_path,poster_path,genre_ids,age_rating
            data = csvMod.find_row("moviesdb.csv", ["title"], {"title": self.name})
            if data:
                self.backdroppath = data["backdrop_path"]
                #moved to loadimages
                #self.backdropimage = self.loadImage(data["backdrop_path"])
                self.posterimage = None#self.loadImage(data["poster_path"])
                self.genre_ids = data["genre_ids"]
                self.age_rating = data["age_rating"]
                self.loaded = True
                return self
        

class TVShowData(VideoData):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def loadImage(self, path):
        pass
    
    def loadImages(self):
        pass
    
    def load(self):
        pass

# function for filtering videos and movies
def filter_videos(videos: list, genres: list, ageraating: str):
    pass

#Creating movie list to import into main.py
WatchHistory = []
WatchList = []
Movies = []
Shows = []

from time import time

#load in all movies into a list
starttime = time()
print("loading movies...")

for row in csvMod.get_all_rows("moviesdb.csv"):
    Movies.append(MovieData(**row))
    
print("done loading, took", str(-starttime+time()), "seconds")

#load in all shows into a list
starttime = time()
print("loading shows...")
for row in csvMod.get_all_rows("shows.csv"):
    Shows.append(TVShowData(**row))
        
print("done loading, took", str(-starttime+time()), "seconds")