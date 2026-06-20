from PIL import Image
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
    def __init__(self, ID, name):
        self.ID = ID
        self.name = name
        self.posterimage = ""
        self.backdropimage = ""
        self.age_rating = ""
        self.genres = []
    
    def loadImage(self, *args): # method to override
        print("override this method in class ", type(self).__name__)
    
    def load(self): # method to override
        pass

class MovieData(VideoData):
    def __init__(self, ID, name):
        super().__init__(ID, name)
    
    def loadImage(self, path):
        ImageURL = "https://image.tmdb.org/t/p/w500" + path
        response = requests.get(ImageURL)
        information = BytesIO(response)
        return Image.open(information)
    
    def load(self):
        #fields are id,title,backdrop_path,poster_path,genre_ids,age_rating
        data = csvMod.find_row("moviesdb.csv", ["title"], {"title": self.name})
        self.backdropimage = self.loadImage(data["backdrop_path"])
        self.posterimage = self.loadImage(data["poster_path"])
        self.genre_ids = data["genre_ids"]
        self.age_rating = data["age_rating"]
        

class TVShowData(VideoData):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def loadImage(self, path):
        pass
    
    def load(self):
        pass
        

#Creating movie list to import into main.py
Movies = []
for row in csvMod.get_all_rows("moviesdb.csv"):
    Movies.append(MovieData(row["id"], row["title"]))