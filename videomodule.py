from threading import Thread
from PIL import Image
from PIL import UnidentifiedImageError
import csvmodule as csvMod
import requests
from io import BytesIO

# ids from https://www.themoviedb.org/talk/5daf6eb0ae36680011d7e6ee
videogenres = {
    "28" : "Action" ,
    "12" : "Adventure" ,
    "16" : "Animation" ,
    "35" : "Comedy" ,
    "80" : "Crime" ,
    "99" : "Documentary" ,
    "18" : "Drama" ,
    "10751" : "Family" ,
    "14" : "Fantasy" ,
    "36" : "History" ,
    "27" : "Horror" ,
    "10402" : "Music" ,
    "9648" : "Mystery" ,
    "10749" : "Romance" ,
    "878" : "Science Fiction" ,
    "10770" : "TV Movie" ,
    "53" : "Thriller" ,
    "10752" : "War" ,
    "37" : "Western" ,
    "10759" : "Action & Adventure" ,
    "10762" : "Kids" ,
    "10763" : "News" ,
    "10764" : "Reality" ,
    "10765" : "Sci-Fi & Fantasy" ,
    "10766" : "Soap" ,
    "10767" : "Talk" ,
    "10768" : "War & Politics" 
}

# classes and functions related to videos 
# e.g. filtering
class VideoData:
    """
    Base class for tv shows and movies
    """
    AgeRatings = {"G": 0,"PG": 0,"M" : 12,"MA15+": 15,"R": 18}
    def __init__(self, id:str, title:str, backdrop_path="", age_rating="", genre_ids="", genres="", **kwargs):
        self.id :str = id
        self.name :str = title
        self.backdroppath :str = backdrop_path
        self.backdropimage :Image = None
        self.age_rating :str = age_rating
        self.genres :list[str] = []
        genre_ids = genre_ids.replace("]", "").replace("[", "").split(", ")
        genres = genres.split("/")
        for genre_id in genre_ids:
            if videogenres.get(genre_id):
                self.genres.append(videogenres.get(genre_id))
        self.genres += genres
        self.loaded :bool = (id != None and title != None and backdrop_path != "" and age_rating != "" and (genre_ids != "" or genres != ""))
    
    def load(self): # method to override
        pass
    
    def loadImage(self, path:str):
        """
        Return an 200-wide image from a tmdb path
        """
        if path:
            try:
                ImageURL = "https://image.tmdb.org/t/p/w200" + path
                response = requests.get(ImageURL)
                information = BytesIO(response.content)
                return Image.open(information)
            except UnidentifiedImageError:
                print("path", path, "could not be found")
    
    def loadImages(self):
        """
        Load all images of a video
        """
        if self.loaded and not self.backdropimage and self.backdroppath:
            self.backdropimage = self.loadImage(self.backdroppath)

class MovieData(VideoData):
    """
    Store Movie Data, child class of VideoData
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def load(self): #overrides VideoData.load()
        """
        Load in movie information from a name
        """
        if not self.loaded:
            #fields are id,title,backdrop_path,poster_path,genre_ids,age_rating
            data = csvMod.find_row("moviesdb.csv", ["title"], {"title": self.name})
            if data:
                self.backdroppath = data["backdrop_path"]
                #poster image not in use
                self.posterimage = None#self.loadImage(data["poster_path"])
                self.genre_ids = data["genre_ids"]
                self.age_rating = data["age_rating"]
                self.loaded = True
        return self
        
class TVEpisodeData(VideoData):
    """
    Class stored in TVShowData.episodes attribute which gives information and images for an episode of a season of a show
    """
    def __init__(self, episode_id:str, show:str, season:str, episode_num:str, episode_title:str, backdrop_img:str, *args, **kwargs):
        super().__init__(episode_id, "", backdrop_img, **kwargs)
        self.season:str = season
        self.episode:str = episode_num
        self.showname:str = show
        self.name:str = episode_title

    def loadImages(self):
        self.backdropimage = self.loadImage(self.backdroppath)
    
    def load(self):
        return self

class TVShowData(VideoData):
    """
    Store TV Show data, child class of VideoData
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seasons:str = kwargs.get("number_of_seasons")
        self.episodes:list[TVEpisodeData] = []
        if not kwargs.get("number_of_seasons"):
            self.loaded = False
        if self.loaded:
            self.loadEpisodes()
    
    def loadEpisodes(self):
        """
        Load in all episodes of a tvshow, returns self
        """
        
        prevFound = True
        row = None
        season = 0
        episode = 1
        
        while prevFound != False:
            if not row: # if there is no episode
                prevFound = False
                season += 1 # check if there is another season
                episode = 1
                
            else: # if there is an episode
                episode += 1 # check if there is a next episode
                
            row = csvMod.find_row("episodes.csv", ["show", "season", "episode_num"],
                                        {"show": self.name,
                                         "season": str(season),
                                         "episode_num": str(episode)})
            if row: 
                print(self.name, "season", season, "episode", episode, "found")
                self.episodes.append(TVEpisodeData(age_rating=self.age_rating,**row))
                prevFound = True
        return self
    
    def loadEpisodeImages(self):
        """
        Load the images for all episodes in a TVShow
        """
        # used https://stackoverflow.com/questions/34512646/how-to-speed-up-api-requests
        threads = []
        for episode in self.episodes:
            threads.append(Thread(target=episode.loadImages))
            threads[-1].start()
            
        for thread in threads:
            thread.join()
        return self
            
    
    def load(self):
        """
        load in information with the title of a show
        """
        if not self.loaded:
            #fields are id,title,backdrop_path,poster_path,genre_ids,age_rating
            data = csvMod.find_row("shows.csv", ["title"], {"title": self.name})
            if data:
                self.backdroppath = data["backdrop_path"]
                self.seasons = data["number_of_seasons"]
                self.posterimage = None
                self.genre_ids = data["genre_ids"]
                self.age_rating = data["age_rating"]
                self.loaded = True
        return self

# function for filtering videos and movies
def filter_videos(videos: list[VideoData], genres: list[str], ageratings: list[str]):
    """
    Return a list of videos from a genres and within a set of ageratings
    """
    indexes = []
    for i in range(len(videos)):
        video = videos[i]
        for genre in video.genres:
            if genre in genres:
                if video.age_rating in ageratings:
                    videos[i].loadImages()
                    indexes.append(i)
                    break
    return [videos[x] for x in indexes]

def videos_from_ids(ids:list[str]):
    '''
    Return videos from a list of ids
    '''
    found = []
    for movie in Movies + Shows:
        if movie.id in ids:
            found.append(movie)
    for show in Shows:
        if show.id in ids:
            found.append(show)
    
    # prevent indexerror by placing temporary values at each index
    reorderedfound = list(range(len(ids)))
    
    # retain the ordering of the ids parameter by putting the movie of each id
    # back into its original place
    for video in found:
        if "Movie" in type(video).__name__:
            reorderedfound[ids.index(video.id)] = video
        elif "Show" in type(video).__name__:
            reorderedfound[ids.index(video.id)] = video
    
    resultlist = []
    for value in reorderedfound:
        if not type(value) == int:
            resultlist.append(value)
        
    return resultlist

#Creating movie list to import into main.py
Movies = []
Shows = []

from time import time

#load in all movies into a list
starttime = time()
print("loading movies...")

for row in csvMod.get_all_rows("moviesdb.csv"):
    Movies.append(MovieData(**row))

threads = []
for movie in Movies:
    threads.append(Thread(target=movie.loadImages))
    threads[-1].start()

for thread in threads:
    thread.join()

print("done loading movies, took", str(-starttime+time()), "seconds")

#load in all shows into a list
starttime = time()
print("loading shows...")

for row in csvMod.get_all_rows("shows.csv"):
    Shows.append(TVShowData(**row))
    
threads = []
for show in Shows:
    threads.append(Thread(target=show.loadImages))
    threads[-1].start()

for thread in threads:
    thread.join()
        
print("done loading shows, took", str(-starttime+time()), "seconds")