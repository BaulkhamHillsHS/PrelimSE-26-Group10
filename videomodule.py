from threading import Thread
from PIL import Image
from PIL import UnidentifiedImageError
import csvmodule as csvMod
import requests
from io import BytesIO

genres = {
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
    def __init__(self, id, title, backdrop_path="", age_rating="", genre_ids="", **kwargs):
        self.id = id
        self.name = title
        self.backdroppath = backdrop_path
        self.backdropimage = None
        self.age_rating = age_rating
        self.genres = []
        genre_ids = genre_ids.replace("]", "").replace("[", "").split(", ")
        for genre_id in genre_ids:
            if genres.get(genre_id):
                self.genres.append(genres.get(genre_id))
        self.loaded = (id and title and backdrop_path and age_rating and genre_ids) or False
    
    def loadGenres(self): #convert numbers to genres
        pass
    
    def load(self): # method to override
        pass
    
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
        if self.loaded and not self.backdropimage and self.backdroppath:
            self.backdropimage = self.loadImage(self.backdroppath)

class MovieData(VideoData):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
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
        
class TVEpisodeData:
    def __init__(self, episode_id, show, season, episode_num, episode_title, backdrop_img, *args, **kwargs):
        self.id = episode_id
        self.show = show
        self.season = season
        self.episode = episode_num
        self.title = episode_title
        self.backdroppath = backdrop_img
    
    def loadImage(self):
        path = self.backdroppath
        if path:
            try:
                ImageURL = "https://image.tmdb.org/t/p/w200" + path
                response = requests.get(ImageURL)
                information = BytesIO(response.content)
                return Image.open(information)
            except UnidentifiedImageError:
                print("path", path, "could not be found")
            return self

class TVShowData(VideoData):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seasons = kwargs.get("number_of_seasons")
        self.episodes = []
        if not kwargs.get("number_of_seasons"):
            self.loaded = False
        if self.loaded:
            self.loadEpisodes()
    
    def loadEpisodes(self):

        prevFound = True
        row = None
        season = 0
        episode = 1
        while prevFound != False:
            if not row:
                prevFound = False
                season += 1
                episode = 1
            else:
                episode += 1
                
            row = csvMod.find_row("episodes.csv", ["show", "season", "episode_num"],
                                        {"show": self.name,
                                         "season": str(season),
                                         "episode_num": str(episode)})
            if row:
                print(self.name, "season", season, "episode", episode, "found")
                self.episodes.append(TVEpisodeData(**row))
                prevFound = True
        return self
    
    def loadEpisodeImages(self):
        threads = []
        for episode in self.episodes:
            threads.append(Thread(target=episode.loadImage))
            threads[-1].start()
            
        for thread in threads:
            thread.join()
        return self
            
    
    def load(self):
        if not self.loaded:
            #fields are id,title,backdrop_path,poster_path,genre_ids,age_rating
            data = csvMod.find_row("moviesdb.csv", ["title"], {"title": self.name})
            if data:
                self.backdroppath = data["backdrop_path"]
                self.seasons = data["number_of_seasons"]
                self.posterimage = None
                self.genre_ids = data["genre_ids"]
                self.age_rating = data["age_rating"]
                self.loaded = True
        return self

# function for filtering videos and movies
def filter_videos(videos: list, genres: list, agerating: int):
    indexes = []
    for i in range(len(videos)):
        video = videos[i]
        for genre in genres:
            if genre in video.genres:
                if VideoData.AgeRatings[video.age_rating] <= agerating:
                    videos[i].loadImages()
                    indexes.append(i)
                    break
    return [videos[x] for x in indexes]

def videos_from_ids(ids):
    found = []
    for movie in Movies:
        if movie.id in ids:
            found.append(movie)
    for show in Shows:
        if show.id in ids:
            found.append(show)
    
    newfoundlist = []
    for video in found:
        newfoundlist[ids.index(video.id)] = video
        
    return newfoundlist

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
    Shows.append(TVShowData(**row).loadEpisodes())
    
threads = []
for show in Shows:
    threads.append(Thread(target=show.loadImages))
    threads[-1].start()

for thread in threads:
    thread.join()
        
print("done loading shows, took", str(-starttime+time()), "seconds")