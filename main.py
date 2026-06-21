# main file for displaying GUI components
import customtkinter as ctk
import tkinter as tk
import accountmodule as AccMod
import videomodule as VidMod
import pyotp
import smtplib
from PIL import Image #used for profile images
from tkinter import messagebox

class FontStyle:
    Title = ("Arial", 40)
    Subtitle = ("Arial", 20)
    Text = ("Arial", 14)

class ColourScheme: # for colours that won't change throughout whole app
    #temporary (looks very bad)
    Primary = "#2d8a1f"
    Secondary = "#dee60e"
    Foreground = "#161616"
    Background = "#000000"
    
    Text = "#dddddd"  
    Red = "red"
    Button = "#EF8606"
    ButtonHover = "#844A04"

# widgets
class BrowsingVideoWidget(ctk.CTkFrame):
    '''
    Widget that displays a movie with a button to select it
    When the button is clicked, it fires a _video_select_event function
    (make sure the parent has a function called _video_select_event)
    '''
    
    def __init__(self, master, data, width=300, height=200, *args, **kwargs):
        super().__init__(master, *args, width=width,height=height, **kwargs)
        self.data = data
        self._build_ui(width, height)
    
    def _video_select(self):
        self.master._video_select_event(self.data)
    
    def _build_ui(self, width, height):
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0,1,2,3,4,5,6), weight=1)
        
        self.namelabel = ctk.CTkLabel(self, text=self.data.name,font=FontStyle.Text,text_color=ColourScheme.Text,fg_color=ColourScheme.Background)
        self.namelabel.grid(column=0,row=0,sticky="nesw")
        
        self.selectbutton = ctk.CTkButton(self, text="",image=ctk.CTkImage(self.data.backdropimage, self.data.backdropimage,size=(width, int(height * 5/7))),command = lambda: self._video_select(),fg_color=ColourScheme.Button,hover_color=ColourScheme.ButtonHover)
        self.selectbutton.grid(column=0,row=1,rowspan=5,sticky="nesw")
        
        info = self.data.age_rating
        for genre in self.data.genres:
            info += ", " + genre
            
        self.infolabel = ctk.CTkLabel(self, text=info,font=FontStyle.Text,text_color=ColourScheme.Text,fg_color=ColourScheme.Background)
        self.infolabel.grid(column=0,row=6,sticky="nesw")

class VideoScrollFrameWidget(ctk.CTkFrame):
    '''
    A horizontally scrolling frame which holds browsingvideowidgets
    '''
    
    def __init__(self, master, title: str, videos: list[VidMod.VideoData], *args, width=2000, **kwargs):
        super().__init__(master, *args, width=width, **kwargs)
        self.width :int = width
        self.title :str = title
        self.videos :list[VidMod.VideoData]= videos
        self._build_ui()
    
    def _video_select_event(self, data):
        self.master._video_select_event(data)
    
    def _build_ui(self):
        self.grid_rowconfigure((0,1,2,3),weight=1)
        self.grid_columnconfigure((0),weight=1)
        self.label = ctk.CTkLabel(self, text=self.title,text_color=ColourScheme.Text,font=FontStyle.Subtitle,fg_color=ColourScheme.Foreground)
        self.label.grid(row=0,column=0,sticky="w")
        
        #hold all the video widgets
        self.scrollableframe = ctk.CTkScrollableFrame(self, width=self.width, fg_color=ColourScheme.Foreground,orientation="horizontal")
        self.scrollableframe.grid(row=1,rowspan=3,column=0, sticky="nesw")
        self.scrollableframe._video_select_event = self._video_select_event
        
        if self.videos:
            i = 0
            for video in self.videos:
                video = BrowsingVideoWidget(self.scrollableframe,video.load())
                video.grid(row=0,column=i)
                i+=1
        
class ProfileWidget(ctk.CTkFrame):
    '''
    A widget which has a button to select a profile
    when the button is clicked it fires _profile_button_pressed on a ProfilePage
    '''
    
    profileimage = Image.open("Images/userimage.png")
    def __init__(self, master, name, *args, **kwargs):
        super().__init__(master, *args, fg_color=ColourScheme.Foreground, bg_color=ColourScheme.Foreground, **kwargs)
        self.name :str = name
        self._build_ui()
    
    def _button_click(self, widget, name):
        # thiswidget -> profilesframe -> profilepage
        the_profile_page: ProfilePage = widget.master.master
        the_profile_page._profile_button_pressed(name)
    
    def _build_ui(self):
        self.grid_columnconfigure((0),weight=1)
        self.grid_rowconfigure((0,1,2),weight=1)
        
        self.namelabel = ctk.CTkLabel(self,text=self.name,text_color=ColourScheme.Text)
        self.namelabel.grid(column=0,row=0)
        
        self.profileframe = ctk.CTkFrame(self)
        self.profileframe.grid(column=0,row=1,rowspan=2)

        self.profilebutton = ctk.CTkButton(self.profileframe, image=ctk.CTkImage(self.profileimage, self.profileimage,size=(140,140)),height=140,text="",hover_color=ColourScheme.ButtonHover,
                                           command=lambda: self._button_click(self, self.name))
        
        # random formulas to make a profile colour
        num = 0
        for letter in self.name:
            num += (ord(letter)-64) * 1862026
        profile_colour = "#" + hex(num%16777216)[2:]
        profile_colour = profile_colour.capitalize()
        if len(profile_colour) != 7:
            profile_colour = ColourScheme.Primary
        
        self.profilebutton.configure(fg_color=profile_colour)
        self.profilebutton.configure(bg_color=profile_colour)
        self.profilebutton.grid(column=0,row=0)


blacklistednamechars = "/,"
class ProfileCreator(ctk.CTkToplevel): #basically a copy of profile editor
    '''
    Create a new profile
    '''
    
    def __init__(self, profilepage, account, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x400")
        self._fg_color = ColourScheme.Background
        self.focus()
        self.title("Create Profile")
        
        self.profilepage: ProfilePage = profilepage
        self.account: AccMod.Account = account
        self._build_ui()
    
    def _create_profile(self):
        ageentry = self.ageentry.get().strip()
        nameentry = self.nameentry.get().strip()
        error = ""
        
        if nameentry:
            if nameentry in self.account._profilenames:
                    error += "Name already in use "
            if len(nameentry) <= 1:
                error += "Name too short "
            elif len(nameentry) > 12:
                error += "Name too long "
            else:
                for letter in blacklistednamechars:
                    if letter in nameentry:
                        error += "Invalid character (" + letter + ") "
        else:
            error += "No name given "
        
        if ageentry:
            if not ageentry.isdigit():
                error += "Invalid age "
            elif int(ageentry) <= 0:
                error += "Too young "
            elif int(ageentry) >= 150:
                error += "Too old "
        else:
            error += "No age given "
        
        if error != "":
            error = "Error: " + error
        else:
            if messagebox.askyesno("Create Profile", f"Do you want to create profile {nameentry}?"):
                self.account.create_profile(nameentry, ageentry)
                
                self.profilepage._build_profilesframe()
                self.destroy()
            
        self.errorlabel.configure(text=error)    
    
    def _build_ui(self):
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0), weight=1)
        self.frame = ctk.CTkFrame(self,bg_color=ColourScheme.Background,fg_color=ColourScheme.Background)
        self.frame.grid(row=0,column=0,sticky="nesw")
        self.frame.grid_columnconfigure((0, 1), weight=1)
        self.frame.grid_rowconfigure((0, 1, 2, 3), weight=1)
        
        self.namelabel = ctk.CTkLabel(self.frame, text="Name: ",font=FontStyle.Text, text_color=ColourScheme.Text)  
        self.nameentry = ctk.CTkEntry(self.frame)
        self.namelabel.grid(row=0, column=0,sticky="e")
        self.nameentry.grid(row=0, column=1,sticky="w")
        
        self.agelabel = ctk.CTkLabel(self.frame, text="Age: ", font=FontStyle.Text, text_color=ColourScheme.Text)
        self.ageentry = ctk.CTkEntry(self.frame)
        self.agelabel.grid(row=1, column=0,sticky="e")
        self.ageentry.grid(row=1, column=1,sticky="w")
        
        self.errorlabel = ctk.CTkLabel(self.frame, text="", font=FontStyle.Text, text_color=ColourScheme.Text)
        self.errorlabel.grid(row=2,column=0,columnspan=2)
        
        self.savebutton = ctk.CTkButton(self.frame, text="Create Profile", fg_color=ColourScheme.Button, hover_color=ColourScheme.ButtonHover, command=self._create_profile)
        self.savebutton.grid(row=3,column=0,columnspan=2)

class ProfileEditor(ctk.CTkToplevel):
    '''
    Profile editor
    '''
    
    def __init__(self, profilepage, account, profile, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x400")
        self._fg_color = ColourScheme.Background
        self.focus()
        profilename = profile._profilename
        self.title(profilename + "'s Settings")
        
        self.profilepage: ProfilePage = profilepage
        self.account: AccMod.Account = account
        self.profilename : str = profilename
        self.profile : AccMod.Profile = profile
        
        self.profile_is_new = True
        if self.profile.exists(): # new profiles cannot be read from csv
            self.profile_is_new = False
        self._build_ui()
    
    def _save_changes(self):
        error = ""
        nameentry = self.nameentry.get().strip()
        ageentry = self.ageentry.get().strip()
        
        if self.profile.load_from_csv():
            
            if nameentry:
                if nameentry in self.account._profilenames:
                    error += "Name already in use "
                if len(nameentry) <= 1:
                    error += "Name too short "
                elif len(nameentry) > 12:
                    error += "Name too long "
                else:
                    for letter in blacklistednamechars:
                        if letter in nameentry:
                            error += "Invalid character (" + letter + ") "
            
            if ageentry:
                if not ageentry.isdigit():
                    error += "Invalid age "
                elif int(ageentry) <= 0:
                    error += "Too young "
                elif int(ageentry) >= 999:
                    error += "Too old "
        
        if ageentry == "DELETE" and nameentry == "DELETE":
            if messagebox.askyesno("Delete Profile", f"Do you want to delete profile {self.profilename}?"):
                self.account.delete_profile(self.profilename)
                self.profilepage._build_profilesframe()
                self.destroy()
        elif error != "":
            error = "Error: " + error
            self.errorlabel.configure(text=error)
        else:
            if messagebox.askyesno("Edit Profile", f"Do you want to edit profile {self.profilename}?"):
                if self.profile_is_new:
                    if nameentry != "" and ageentry != "":
                        self.profile.update_details(nameentry, ageentry)
                    elif nameentry != "":
                        self.profile.update_details(nameentry, self.profile._age)
                    elif ageentry!= "":
                        self.profile.update_details(self.profilename, ageentry)
                else:
                    if nameentry != "" and ageentry != "":
                        self.profile.update_details(nameentry, ageentry, True)
                    elif nameentry != "":
                        self.profile.update_details(nameentry, self.profile._age, True)
                    elif ageentry!= "":
                        self.profile.update_details(self.profilename, ageentry, True)
                
                self.profilepage._build_profilesframe()
                self.destroy()
           
    def _build_ui(self):
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0), weight=1)
        self.frame = ctk.CTkFrame(self,bg_color=ColourScheme.Background,fg_color=ColourScheme.Background)
        self.frame.grid(row=0,column=0,sticky="nesw")
        self.frame.grid_columnconfigure((0, 1), weight=1)
        self.frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        
        self.namelabel = ctk.CTkLabel(self.frame, text=f"Name (currently {self.profilename}): ",font=FontStyle.Text, text_color=ColourScheme.Text)  
        self.nameentry = ctk.CTkEntry(self.frame)
        self.namelabel.grid(row=0, column=0,sticky="e")
        self.nameentry.grid(row=0, column=1,sticky="w")
        
        self.agelabel = ctk.CTkLabel(self.frame, text=f"Age (currently {self.profile._age}): ", font=FontStyle.Text, text_color=ColourScheme.Text)
        self.ageentry = ctk.CTkEntry(self.frame)
        self.agelabel.grid(row=1, column=0,sticky="e")
        self.ageentry.grid(row=1, column=1,sticky="w")
        
        self.errorlabel = ctk.CTkLabel(self.frame, text="", font=FontStyle.Text, text_color=ColourScheme.Text)
        self.errorlabel.grid(row=2,column=0,columnspan=2)
        
        self.tutoriallabel = ctk.CTkLabel(self.frame, text="Type DELETE into both boxes to delete an account", font=FontStyle.Text, text_color=ColourScheme.Text)
        self.tutoriallabel.grid(row=3,column=0,columnspan=2)
        
        self.savebutton = ctk.CTkButton(self.frame, text="Save Changes", fg_color=ColourScheme.Button, hover_color=ColourScheme.ButtonHover, command=self._save_changes)
        self.savebutton.grid(row=4,column=0,columnspan=2)
        # name, movie rating

#pages    
class StandardPage(ctk.CTkFrame):
    """
    Parent class for pages that can be accessed when in a profile
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, fg_color=ColourScheme.Background, **kwargs)
        self._build_header()
    
    def _build_header(self):
        logo = Image.open("Images/appname_ss_logo.png")
        self.grid_columnconfigure((0,1,), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        
        self.headerframe = ctk.CTkFrame(self,fg_color=ColourScheme.Foreground)
        self.headerframe.grid(row=0,column=0,columnspan=100,sticky="nesw")
        
        self.logo = ctk.CTkLabel(self.headerframe, text="",image=ctk.CTkImage(logo,logo,size=(100,100)))
        self.logo.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        
        def goMenuPage():
            app._change_page("MenuPage")
    
        self.menu_button = ctk.CTkButton(self.headerframe, text="Menu",fg_color=ColourScheme.Button,bg_color=ColourScheme.Foreground,hover_color=ColourScheme.ButtonHover, command=goMenuPage)
        self.menu_button.grid(row=0, column=2, padx=10, pady=10, sticky="ne")
        
    
    def _build_ui(self): #method to be overwritten (DON'T TOUCH THIS)
        pass
        

#pages after picking a profile
class VideoPage(StandardPage):
    """
    Screen to display when selecting a movie/show
    """
    def __init__(self, master, videodata, showdata=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.showdata: VidMod.TVShowData = showdata
        self.videodata : VidMod.VideoData = videodata
        self._build_ui()
    
    
    def _build_ui(self):
        def watchlist_button_event():
            if self.videodata.id not in self.master.profile._watchlist:
                self.master.profile._watchlist.append(self.videodata.id)
                self.watchlistbutton.configure(text="Remove from watchlist")
            else:
                self.master.profile._watchlist.remove(self.videodata.id)
                self.watchlistbutton.configure(text="Add to watchlist")
    
        def watch_video():
            if "tv" in type(self.videodata).__name__.lower(): #tvepisodedata
                id = self.videodata.id.partition("_")[0]
                # episodeid looks like 871727_SO1E02 so this gets only the id which is identical to the show id
                if id not in self.master.profile._history:
                    self.master.profile._history.append(id)
            
            else:
                if self.videodata.id not in self.master.profile._history:
                    self.master.profile._history.append(self.videodata.id)
                
        def change_to_previous_page():
            if self.showdata:
                self.master._change_page("TVShowPage", self.showdata)
            else:
                self.master._change_page("BrowsingPage")
        
        self.grid_columnconfigure((0),weight=1)
        self.grid_rowconfigure((0),weight=1)
        self.imagelabel = ctk.CTkLabel(self, text="",image=ctk.CTkImage(self.videodata.backdropimage, size=(720,480)))
        self.imagelabel.grid(row=1,column=0,columnspan=2)
        
        if not "tv" in type(self.videodata).__name__.lower():
            # don't add the add to watch list button
            self.watchlistbutton = ctk.CTkButton(self,fg_color=ColourScheme.Button,hover_color=ColourScheme.ButtonHover,command=watchlist_button_event)
            
            if self.videodata.id in self.master.profile._watchlist:
                self.watchlistbutton.configure(text="Remove from watchlist")
            else:
                self.watchlistbutton.configure(text="Add to watchlist")
            self.watchlistbutton.grid(row=2,column=0,sticky="se")
        
        self.watchbutton = ctk.CTkButton(self,text="Watch Video", fg_color=ColourScheme.Button,hover_color=ColourScheme.ButtonHover,command=watch_video)
        self.watchbutton.grid(row=2,column=1,sticky="se")
        
        self.previouspagebutton = ctk.CTkButton(self,text="Return to Previous Page", fg_color=ColourScheme.Button,hover_color=ColourScheme.ButtonHover,command=change_to_previous_page)
        self.previouspagebutton.grid(row=2,column=0,sticky="sw")
            
class TVShowPage(StandardPage):
    '''
    place to pick a tv episode
    '''
    
    def __init__(self, master, tvshowdata: VidMod.TVShowData, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        tvshowdata.loadEpisodeImages()
        self.tvshowdata: VidMod.TVShowData = tvshowdata
        self._build_ui()
    
    def _video_select_event(self, data):
            self.master._change_page("VideoPage", data, self.tvshowdata)
    
    def _build_ui(self):
        def watchlist_button_event():
            if self.tvshowdata.id not in self.master.profile._watchlist:
                self.master.profile._watchlist.append(self.tvshowdata.id)
                self.watchlistbutton.configure(text="Remove from watchlist")
            else:
                self.master.profile._watchlist.remove(self.tvshowdata.id)
                self.watchlistbutton.configure(text="Add to watchlist")

        def _back_to_browsingpage():
            self.master._change_page("BrowsingPage")
            
        self.videoswidget = VideoScrollFrameWidget(self, self.tvshowdata.name, self.tvshowdata.episodes,fg_color=ColourScheme.Foreground)
        self.videoswidget.grid(row=1,column=0)
        self.videoswidget._video_select_event = self._video_select_event
        
        self.watchlistbutton = ctk.CTkButton(self,fg_color=ColourScheme.Button,hover_color=ColourScheme.ButtonHover,command=watchlist_button_event)        
        if self.tvshowdata.id in self.master.profile._watchlist:
            self.watchlistbutton.configure(text="Remove from watchlist")
        else:
            self.watchlistbutton.configure(text="Add to watchlist")
        self.watchlistbutton.grid(row=2,column=0,sticky="se")
        
        self.previouspagebutton = ctk.CTkButton(self,text="Return to Previous Page", fg_color=ColourScheme.Button,hover_color=ColourScheme.ButtonHover,command=_back_to_browsingpage)
        self.previouspagebutton.grid(row=2,column=0,sticky="sw")
        
class BrowsingPage(StandardPage):
    '''
    Page to browse through videos
    '''
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_allowed_videos()
        self.filters = []
        self.filterwidgets = {}
        self._build_ui()
    
    def get_allowed_videos(self):
        self.allowedratings : list[str] = list(VidMod.VideoData.AgeRatings.keys())
        for rating in VidMod.VideoData.AgeRatings:
            if VidMod.VideoData.AgeRatings[rating] > int(self.master.profile._age):
                self.allowedratings.remove(rating)
        
        self.shows = VidMod.filter_videos(VidMod.Shows, VidMod.videogenres.values(), self.allowedratings)
        self.movies = VidMod.filter_videos(VidMod.Movies, VidMod.videogenres.values(), self.allowedratings)
        self.watchhistory = VidMod.filter_videos(VidMod.videos_from_ids(self.master.profile._history), VidMod.videogenres.values(), self.allowedratings)
        self.watchlist = VidMod.filter_videos(VidMod.videos_from_ids(self.master.profile._watchlist), VidMod.videogenres.values(), self.allowedratings)
    
    def apply_filters(self):
        screenwidth = self.master.winfo_screenwidth()
        screenheight = self.master.winfo_screenheight()
        self.frameinscrollframe.destroy()
        
        self.frameinscrollframe = ctk.CTkFrame(self.verticalscrollframe, fg_color=ColourScheme.Background)
        self.frameinscrollframe.grid(row=0,column=0,sticky="nesw")
        self.frameinscrollframe._video_select_event = self._video_select_event
        
        self.showscrollframe = VideoScrollFrameWidget(self.frameinscrollframe, "TV Shows", VidMod.filter_videos(self.shows, self.filters, self.allowedratings), fg_color=ColourScheme.Foreground,width=screenwidth)
        self.showscrollframe.grid(row=1,column=0, sticky="nesw")
        self.moviescrollframe = VideoScrollFrameWidget(self.frameinscrollframe, "Movies", VidMod.filter_videos(self.movies, self.filters, self.allowedratings), fg_color=ColourScheme.Foreground,width=screenwidth)
        self.moviescrollframe.grid(row=2,column=0, sticky="nesw")
        
        self.watchhistoryscrollframe = VideoScrollFrameWidget(self.frameinscrollframe, "Watch History", VidMod.filter_videos(self.watchhistory, self.filters, self.allowedratings), fg_color=ColourScheme.Foreground,width=screenwidth)
        self.watchhistoryscrollframe.grid(row=3,column=0,sticky="nesw")
        
        self.watchlistscrollframe = VideoScrollFrameWidget(self.frameinscrollframe, "Watch List", VidMod.filter_videos(self.watchlist, self.filters, self.allowedratings), fg_color=ColourScheme.Foreground,width=screenwidth)
        self.watchlistscrollframe.grid(row=4,column=0, sticky="nesw")
    
    def add_filter(self):
        addedfilter = self.filterbox.get()
        if addedfilter:
            if addedfilter not in self.filters:
                self.filters.append(addedfilter)
                filterwidget = ctk.CTkButton(self.filterframe,text="X " + addedfilter, text_color=ColourScheme.Text, fg_color=ColourScheme.Button,hover_color=ColourScheme.Red,command=lambda: self.remove_filter(addedfilter))
                filterwidget.grid(column=len(self.filterwidgets),row=0)
                self.filterwidgets[addedfilter] = filterwidget
            else:
                messagebox.showwarning('Filter has not been applied', 'Filter already applied')
    
    def remove_filter(self, filter_to_remove):
        self.filters.remove(filter_to_remove)
        if self.filterwidgets.get(filter_to_remove):
            self.filterwidgets[filter_to_remove].destroy()
            self.filterwidgets.pop(filter_to_remove)
    
    def _video_select_event(self, videodata):
        if "show" in type(videodata).__name__.lower():
            self.master._change_page("TVShowPage", videodata)
        else:
            self.master._change_page("VideoPage", videodata)
    
    def _build_ui(self):
        screenwidth = self.master.winfo_screenwidth()
        screenheight = self.master.winfo_screenheight()
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)
        
        self.filterbox = ctk.CTkComboBox(self, fg_color=ColourScheme.Foreground)
        self.filterbox.configure(values=list(VidMod.videogenres.values()))
        self.filterbox.grid(row=1,column=0,sticky="w")
        
        self.addfilterbutton = ctk.CTkButton(self, text="Add Filter", fg_color=ColourScheme.Button,hover_color=ColourScheme.ButtonHover,command=self.add_filter)
        self.addfilterbutton.grid(row=1,column=0)
        
        self.applyfilterbutton = ctk.CTkButton(self, text="Apply Filters", fg_color=ColourScheme.Button,hover_color=ColourScheme.ButtonHover,command=self.apply_filters)
        self.applyfilterbutton.grid(row=1,column=0,sticky="e")
        
        self.filterframe = ctk.CTkScrollableFrame(self, fg_color=ColourScheme.Foreground,width=screenwidth,height=20,orientation="horizontal")
        self.filterframe.grid(row=2,column=0)
        
        self.verticalscrollframe = ctk.CTkScrollableFrame(self, fg_color=ColourScheme.Background,width=screenwidth, height=screenheight*4/7)
        self.verticalscrollframe.grid(row=3, rowspan=6,column=0,sticky="w")
        self.verticalscrollframe.grid_rowconfigure((0, 1,2,3,4),weight=1)
        self.verticalscrollframe._video_select_event = self._video_select_event
        
        self.frameinscrollframe = ctk.CTkFrame(self.verticalscrollframe, fg_color=ColourScheme.Background)
        self.frameinscrollframe.grid(row=0,column=0,sticky="nesw")
        self.frameinscrollframe._video_select_event = self._video_select_event
        
        self.showscrollframe = VideoScrollFrameWidget(self.frameinscrollframe, "TV Shows", self.shows, fg_color=ColourScheme.Foreground,width=screenwidth)
        self.showscrollframe.grid(row=1,column=0, sticky="nesw")
        
        self.moviescrollframe = VideoScrollFrameWidget(self.frameinscrollframe, "Movies", self.movies, fg_color=ColourScheme.Foreground,width=screenwidth)
        self.moviescrollframe.grid(row=2,column=0, sticky="nesw")
        
        self.watchhistoryscrollframe = VideoScrollFrameWidget(self.frameinscrollframe, "Watch History", self.watchhistory, fg_color=ColourScheme.Foreground,width=screenwidth)
        self.watchhistoryscrollframe.grid(row=3,column=0,sticky="nesw")
        
        self.watchlistscrollframe = VideoScrollFrameWidget(self.frameinscrollframe, "Watch List", self.watchlist, fg_color=ColourScheme.Foreground,width=screenwidth)
        self.watchlistscrollframe.grid(row=4,column=0, sticky="nesw")
    
#starting page    
class LoginPage(ctk.CTkFrame):
    '''
    Page to login to an account
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, fg_color=ColourScheme.Background, bg_color=ColourScheme.Background, **kwargs)
        self._build_ui()
    
    def _goToStreamingApp(self, userAccount):
        self.master.account = userAccount
        app._change_page("ProfilePage")
        

    def _2FactAuth(self, userAccount, user_email):
        
        for widget in self.winfo_children():
                widget.destroy()   
        self.grid_columnconfigure((0,1,2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        
        #build page elements
        self.logo = ctk.CTkLabel(self, text="",image=ctk.CTkImage(Image.open("Images/appname_ss_logo.png"),size=(100,100)))
        self.logo.grid(row=0, column=0, padx=10, pady=10, sticky="n")
        
        self.label = ctk.CTkLabel(self, text="AppName Streaming Service", text_color=ColourScheme.Text, font=("arial", 40))
        self.label.grid(row=0, column=1, padx=10, pady=15, sticky="ew")
            
        self.label = ctk.CTkLabel(self, text="A six digit code has been sent to your email. If you do not see it please check spam. ", text_color=ColourScheme.Text, font=("arial", 20))
        self.label.grid(row=1, column=1, padx=20, pady=5, sticky="ew")
        
        self.code_entry = ctk.CTkEntry(self, placeholder_text="XXXXXX", height=30)
        self.code_entry.grid(row=2, column=1, padx=20, pady=5, sticky="ew")
    
        self.submit_button = ctk.CTkButton(self, text="Submit", fg_color=ColourScheme.Button, hover_color=ColourScheme.ButtonHover, command= lambda: checkUsercode(self.code_entry.get(), code))
        self.submit_button.grid(row=3, column=1, padx=40, pady=5, sticky="ew")

        #send email
        email = "devashreepatel95@gmail.com" #usually company email
        receiver_email = user_email
        key = pyotp.random_base32()
        code = str(pyotp.TOTP(key).now())
        email_message = f"Subject: APPNAME STREAMING SERVICE SIX-DIGIT CODE \n\n Your one time six digit code is: {code}"
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email,"luruzlexucsjtmjg")
        
        # the line below is temporarily disabled as I do not want to send 5 million emails
        # to random accounts while testing out other functions!
        server.sendmail(email, receiver_email, email_message)
        #code = "123456"

        def checkUsercode(usercode, code):    
            if usercode == code:
                self._goToStreamingApp(userAccount)
            else:
                messagebox.showwarning('Incorrect Code', 'This code is not correct')

            
    def Login(self, email, password):  
        #uses  account modules login function to check if account exists
        userAccount = AccMod.login(email.lower(), password)
        if userAccount != False:
            messagebox.showwarning('Login Successful', 'You have sucessfully logged in!')
            self._2FactAuth(userAccount, email)                        
        elif not email or not password: 
            messagebox.showwarning('Details Missing', 'Please enter both email and password')
        else:
            messagebox.showwarning('Account not found', 'Please enter valid credentials')
        
    
    def _build_ui(self):
        logo = Image.open("Images/appname_ss_logo.png")
        self.grid_columnconfigure((0,1,2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        
        self.label = ctk.CTkLabel(self, text="AppName Streaming Service", text_color=ColourScheme.Text, font=("arial", 40))
        self.label.grid(row=0, column=1, padx=20, pady=30, sticky="ew")
        
        self.logo = ctk.CTkLabel(self, text="",image=ctk.CTkImage(logo, logo,size=(100,100)))
        self.logo.grid(row=0, column=1, padx=10, pady=10, sticky="w")
                
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Enter your email", height=30)
        self.email_entry.grid(row=1,column=1,padx=20,pady=5, sticky= "ew")
        
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Enter your password", height=30)
        self.password_entry.grid(row=2, column=1, padx=20, pady=5, sticky="ew")
        
        self.login_button = ctk.CTkButton(self, text="Login", fg_color=ColourScheme.Button, hover_color=ColourScheme.ButtonHover, command=lambda: self.Login(self.email_entry.get(), self.password_entry.get()))
        self.login_button.grid(row=3, column=1, padx=100, pady=5, sticky="ew")

#page after logging into an account
# I need to fix it as it doesnt immeditatley load the updataed plan + it needs to print a TXT recpiet file
class SubscriptionManagementPage(ctk.CTkFrame):
    '''
    Page to edit account subscription
    '''
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, fg_color=ColourScheme.Background, bg_color=ColourScheme.Background, **kwargs)
        self._build_ui()
    def _build_ui(self):
        account : AccMod.Account = self.master.account
        self.grid_columnconfigure((0,1,2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        
        self.label = ctk.CTkLabel(self, text="Manage Subscription", text_color=ColourScheme.Text, font=("arial", 40))
        self.label.grid(row=0, column=1, padx=20, pady=30, sticky="ew")
        
        def button_event():
            app._change_page("ProfilePage")

        self.return_button = ctk.CTkButton(self, text="Return to Profiles", command=button_event)
        self.return_button.grid(row=0, column=2, padx=0, pady=15, sticky="ne")

        account_plan = f"The Current Account Plan: {account._plan}"
        self.current_acc_plan = ctk.CTkLabel(self, text=account_plan, text_color=ColourScheme.Text, font=("arial", 20))
        self.current_acc_plan.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
        
        self.text = ctk.CTkLabel(self, text="Plans Available", text_color=ColourScheme.Text, font=("arial", 20))
        self.text.grid(row=2, column=1, padx=10, pady=8, sticky="ew")
        
        def change_to_free():
            if messagebox.askyesno('Change Plan', 'Change current plan to Free Plan?'):
                account.update_plan("FreePlan")
                fh = open('subscription_invoice.txt', 'w')
                fh.write(f'-SUBSCRIPTION INVOICE- \nFrom: AppName Streaming Service\nBill to: {account.name}\nService: Free Plan \nRate: $0.00/month\nTotal: $0.00')
                fh.close()
                app._change_page("SubscriptionManagementPage")
                
                 
        self.free_button = ctk.CTkButton(self, text="Free Plan: $0.00/month", fg_color=ColourScheme.Button, hover_color=ColourScheme.ButtonHover, command=change_to_free)
        self.free_button.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        def change_to_standard():
            if messagebox.askyesno('Change Plan', 'Change current plan to Standard Plan?'):
                account.update_plan("StandardPlan")
                fh = open('subscription_invoice.txt', 'w')
                fh.write(f'-SUBSCRIPTION INVOICE- \nFrom: AppName Streaming Service\nBill to: {account.name}\nService: Standard Plan \nRate: $11.99/month\nTotal: $11.99')
                fh.close()
                app._change_page("SubscriptionManagementPage")
            
            
        self.standard_button = ctk.CTkButton(self, text="Standard Plan: $11.99/month", fg_color=ColourScheme.Button, hover_color=ColourScheme.ButtonHover, command=change_to_standard)
        self.standard_button.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        
        def change_to_premium():
            if messagebox.askyesno('Change Plan', 'Change current plan to Premium Plan?'):
                account.update_plan("PremiumPlan")
                fh = open('subscription_invoice.txt', 'w')
                fh.write(f'-SUBSCRIPTION INVOICE- \nFrom: AppName Streaming Service\nBill to: {account.name}\nService: Premium Plan \nRate: $15.99/month\nTotal: $15.99')
                fh.close()
                app._change_page("SubscriptionManagementPage")           
            
        self.premium_button = ctk.CTkButton(self, text="Premium Plan: $15.99/month", fg_color=ColourScheme.Button, hover_color=ColourScheme.ButtonHover, command=change_to_premium)
        self.premium_button.grid(row=5, column=1, padx=10, pady=5, sticky="ew")
        
        ## popup that ask you if you are sure that you want to change the plan
        ## txt file showing supscription invoice after change of plan
        
class MenuPage(ctk.CTkFrame):
    '''
    Homepage for a profile
    '''
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, fg_color=ColourScheme.Background, bg_color=ColourScheme.Background, **kwargs)
        self._build_ui()
    def _build_ui(self):
        self.logo = ctk.CTkLabel(self, text="",image=ctk.CTkImage(Image.open("Images/appname_ss_logo.png"),size=(100,100)))
        self.logo.grid(row=0, column=1, padx=10, pady=10, sticky="n")
        account : AccMod.Account = self.master.account
        self.grid_columnconfigure((0,1,2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        
        self.label = ctk.CTkLabel(self, text="MENU", text_color=ColourScheme.Text, font=("arial", 40))
        self.label.grid(row=0, column=1, padx=20, pady=30, sticky="ew")
        
        def go_browsing():
            app._change_page("BrowsingPage")

        self.browse_button = ctk.CTkButton(self, text="Browsing Page", command=go_browsing)
        self.browse_button.grid(row=1, column=1, padx=20, pady=5, sticky="ew")
        
        def view_report():
            account : AccMod.Account = self.master.account
            #profiles: list[AccMod.Profile] = AccMod.returnProfiles(account)
            profiles = account._profiles
            view_log = ""
            for profile in profiles:
                view_log = view_log + profile._profilename + " - viewing history: "
                show_names = VidMod.videos_from_ids(profile._history)
                for show in show_names:
                    view_log = view_log + show.name + ", "
                view_log = view_log + "\n"
            view_log = view_log[:-3]
            fh = open('acc_viewing_report.txt', 'w')
            fh.write(view_log)
            fh.close()

            
        self.watchlist_button = ctk.CTkButton(self, text="Download Viewing Report", command=view_report)
        self.watchlist_button.grid(row=2, column=1, padx=20, pady=5, sticky="ew")
        
        def return_profile():
            app._change_page("ProfilePage")

        self.return_button = ctk.CTkButton(self, text="Return to Profiles", command=return_profile)
        self.return_button.grid(row=3, column=1, padx=20, pady=5, sticky="ew")
        
        def exit_application():
           pass

        self.exit_button = ctk.CTkButton(self, text="Exit Application", command=self.master.destroy)
        self.exit_button.grid(row=4, column=1, padx=20, pady=5, sticky="ew")
        
        
        
        
class ProfilePage(ctk.CTkFrame):
    '''
    Page for selecting a profile
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, fg_color=ColourScheme.Background, bg_color=ColourScheme.Background, **kwargs)
        self.account : AccMod.Account = self.master.account
        self.profilesframe = None
        self._build_ui()
        self.edit_profile = False
    
    def _profile_button_pressed(self, profilename:str):
        '''
        Function that fires when a profile button is pressed
        '''
        
        if self.edit_profile:
            # enter the profile editor
            editedprofile = None
            for profile in self.master.account._profiles:
                if profile._profilename == profilename:
                    editedprofile = profile
            ProfileEditor(self, self.master.account, editedprofile)
        else:
            # enters menu page with the profile
            for profile in self.master.account._profiles:
                if profile._profilename == profilename:
                    self.master.profile = profile
                    break
            self.master._change_page("MenuPage")
    
    def _build_profilesframe(self):
        if self.profilesframe:
            self.profilesframe.grid_forget()
            for profilewidget in self.profilesframe.winfo_children():
                profilewidget.destroy()
        
        profilenames = self.account._profilenames
        lenprofiles = len(profilenames)
        
        self.profilesframe = ctk.CTkFrame(self, fg_color=ColourScheme.Foreground, bg_color=ColourScheme.Foreground)
        self.profilesframe.grid_columnconfigure(tuple(range(lenprofiles%7+1)), weight=1)
        self.profilesframe.grid_rowconfigure(tuple(range(lenprofiles//7+1)), weight=1)
        
        for i in range(lenprofiles):
            # make a profilewidget for each profile
            profile = ProfileWidget(self.profilesframe, profilenames[i])
            profile.grid(column=i%7, row=i//7)
            
        self.profilesframe.grid(column=1,row=2, columnspan=2)
    
    def _build_ui(self):
        
        self.grid_columnconfigure((0,1,2,3), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self._build_profilesframe()
        
        self.logo = ctk.CTkLabel(self, text="",image=ctk.CTkImage(Image.open("Images/appname_ss_logo.png"),size=(100,100)))
        self.logo.grid(row=0, column=0, padx=10, pady=10, sticky="n")
        
        self.label = ctk.CTkLabel(self, text="Profile Page", text_color=ColourScheme.Text, font=FontStyle.Title)
        self.label.grid(row=0, column=1, columnspan=2, padx=20, pady=30, sticky="ew")
        
        def manageSub():
            app._change_page("SubscriptionManagementPage")

        self.sub_man_button = ctk.CTkButton(self, text="Manage Subscription", command=manageSub)

        def logOut():
            app._change_page("LoginPage")
            app.profile = None
            app.account = None
        
        self.log_out_button = ctk.CTkButton(self, text="Log Out", fg_color="red",hover_color="#941223", command=logOut)
        
        def toggleSettings():
            self.edit_profile = not self.edit_profile
            if self.edit_profile:
                self.settings_button.configure(fg_color="red",hover_color="#941223")
                self.settings_button.configure(text="Click a Profile")
            else:
                self.settings_button.configure(fg_color=ColourScheme.Button, hover_color=ColourScheme.ButtonHover)
                self.settings_button.configure(text="Toggle Settings")
            
        self.settings_button = ctk.CTkButton(self, text="Toggle Settings", fg_color=ColourScheme.Button, hover_color=ColourScheme.ButtonHover, command = toggleSettings)
        
        def openProfileCreator():
            profilecreator = ProfileCreator(self, self.master.account)
        
        self.profilecreator_button = ctk.CTkButton(self, text="New Profile", fg_color=ColourScheme.Button, hover_color=ColourScheme.ButtonHover, command = openProfileCreator)
        self.sub_man_button.grid(row=5, column=0, padx=20, pady=30, sticky="se")
        self.settings_button.grid(row=5, column=1)
        self.profilecreator_button.grid(row=5, column=2)
        self.log_out_button.grid(row=5, column=3, padx=20, pady=30, sticky="sw")
        
# used to map a string to a class (useless)
pages : dict = {"StandardPage": StandardPage, 
                "ProfilePage": ProfilePage,
                "VideoPage": VideoPage,
                "TVShowPage": TVShowPage,
                "BrowsingPage": BrowsingPage, 
                "SubscriptionManagementPage": SubscriptionManagementPage, 
                "LoginPage": LoginPage, 
                "ProfilePage": ProfilePage,
                "MenuPage": MenuPage}

class StreamingApp(ctk.CTk):
    '''
    App that changes pages and stuff
    '''
    
    Title = "App"
    def __init__(self):
        super().__init__()
        self.geometry("10000x10000")
        self.title("App Name Streaming Service")
        self.currentpage: ctk.CTkFrame = None
        self.previouspage: ctk.CTkFrame = None
        self.account : AccMod.Account = None
        self.profile : AccMod.Profile = None
        
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)
    
    def _change_page(self, newpage:str, *args, **kwargs):
        """
        Change the app page being viewed
        """
        # *args, **kwargs is used in VideoPage, where VidMod.VideoData is passed as an argument
        if pages.get(newpage):
            # undisplay the previous page
            if self.currentpage:
                # unplaces the old page
                self.currentpage.grid_remove()
            if self.previouspage:
                self.previouspage.destroy()
                
            # create a new page
            self.previouspage = self.currentpage
            self.currentpage = pages[newpage](self, *args, **kwargs)
            
            # display the new page
            self.currentpage.grid(row=0, column=0, sticky="nesw")
        else:
            raise KeyError(f"Page {newpage} does not exist")
    
    #this method is no longer used anywhere should we delete it???
    def _test_page(self, page):
        """
        See what a page looks like (for testing only)
        """
        if self.currentpage:
            self.currentpage.grid_forget()
            self.currentpage.destroy()
           
        self.currentpage = page
        self.currentpage.grid(row=0, column=0, sticky="nesw")
             
if __name__ == "__main__":
    app = StreamingApp()
    app._change_page("LoginPage")
    app.mainloop()
    
    #run on app close
    if app.account:
        app.account.save_to_csv()
        for profile in app.account._profiles:
            if profile.exists():
                profile.save_to_csv()
            else:
                app.account.create_profile(profile._profilename, profile._age, True)

