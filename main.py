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
class VideoWidget(ctk.CTkFrame):
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
    def __init__(self, master, title: str, videos: list[VidMod.VideoData], *args, width=2000, **kwargs):
        super().__init__(master, *args, width=width, **kwargs)
        self.width = width
        self.title = title
        self.videos = videos
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
                video = VideoWidget(self.scrollableframe,video.load())
                video.grid(row=0,column=i)
                i+=1
        
class ProfileWidget(ctk.CTkFrame):
    profileimage = Image.open("Images/userimage.png")
    def __init__(self, master, name, *args, **kwargs):
        super().__init__(master, *args, fg_color=ColourScheme.Foreground, bg_color=ColourScheme.Foreground, **kwargs)
        self.name = name
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

# ctktoplevels? what do i even call this
blacklistednamechars = "/,"
class ProfileCreator(ctk.CTkToplevel): #basically a copy of profile editor
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
        ageentry = self.ageentry.get()
        nameentry = self.nameentry.get()
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
    def __init__(self, profilepage, account, profilename, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x400")
        self._fg_color = ColourScheme.Background
        self.focus()
        self.title(profilename + "'s Settings")
        
        self.profilepage: ProfilePage = profilepage
        self.account: AccMod.Account = account
        self.profilename = profilename
        self.profile = AccMod.Profile(self.account, self.profilename)
        self.profile.load_from_csv()
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
                if nameentry != "" and ageentry != "":
                    self.profile.update_details(nameentry, ageentry)
                elif nameentry != "":
                    self.profile.update_details(nameentry, self.profile._age)
                elif ageentry!= " ":
                    self.profile.update_details(self.profilename, ageentry)
                
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
    
    def _build_ui(self): #method to be overriden
        pass

#pages after picking a profile
class VideoPage(StandardPage):
    """
    Screen to display when selecting a movie/show
    """
    def __init__(self, master, videodata, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.videodata = videodata
        self._build_ui()
    
    def _build_ui(self):
        self.grid_columnconfigure((0),weight=1)
        self.grid_rowconfigure((0),weight=1)
        #don't use the videowidget class for this page i was just testing
        self.videoimage = VideoWidget(self, self.videodata, width=700,height=500)
        self.videoimage.grid(row=0, column=0)
    
    def insertVideo(self):
        #practice import of an image       
        pass
        
class BrowsingPage(StandardPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._build_ui()
    
    def _video_select_event(self, videodata):
        if videodata.id not in self.master.profile._history:
            if self.master.profile._history == [""]:
                self.master.profile._history = [videodata.id]
            else:
                self.master.profile._history.append(videodata.id)
                
            self.master.profile.save_to_csv()
        self.master._change_page("VideoPage", videodata)
    
    def _build_ui(self):
        screenwidth = self.master.winfo_screenwidth()
        screenheight = self.master.winfo_screenheight()
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)
        self.verticalscrollframe = ctk.CTkScrollableFrame(self, fg_color=ColourScheme.Background,width=screenwidth, height=screenheight*5/7)
        self.verticalscrollframe.grid(row=1, rowspan=7,column=0,sticky="w")
        self.verticalscrollframe.grid_rowconfigure((0, 1,2,3,4),weight=1)
        
        self.showscrollframe = VideoScrollFrameWidget(self.verticalscrollframe, "TV Shows", VidMod.Shows, fg_color=ColourScheme.Foreground,width=screenwidth)
        self.showscrollframe.grid(row=1,column=0, sticky="nesw")
        
        self.moviescrollframe = VideoScrollFrameWidget(self.verticalscrollframe, "Movies", VidMod.Movies, fg_color=ColourScheme.Foreground,width=screenwidth)
        self.moviescrollframe.grid(row=2,column=0, sticky="nesw")
        
        self.watchhistoryscrollframe = VideoScrollFrameWidget(self.verticalscrollframe, "Watch History", VidMod.videos_from_ids(self.master.profile._history), fg_color=ColourScheme.Foreground,width=screenwidth)
        
        self.watchlistscrollframe = VideoScrollFrameWidget(self.verticalscrollframe, "Watch List", VidMod.videos_from_ids(self.master.profile._watchlist), fg_color=ColourScheme.Foreground,width=screenwidth)
        self.watchlistscrollframe.grid(row=4,column=0, sticky="nesw")
        
        self.temporarybutton = ctk.CTkButton(self,text="go to videopage temporary", command=lambda: self._video_select_event(VidMod.MovieData("315162","Puss in Boots: The Last Wish").load()))
        self.temporarybutton.place(x=100,y=100)
    
#starting page    
class LoginPage(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, fg_color=ColourScheme.Background, bg_color=ColourScheme.Background, **kwargs)
        self._build_ui()
    
    def goToStreamingApp(self, userAccount):
        self.master.account = userAccount
        app._change_page("ProfilePage")
        

    def twoFactAuth(self, userAccount, user_email):
        
        for widget in self.winfo_children():
                widget.destroy()   
        self.grid_columnconfigure((0,1,2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        
        #build page elements
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
        #server.sendmail(email, receiver_email, email_message)

        def checkUsercode(usercode, code):    
            #if usercode == code:
            if usercode == "123456":
                self.goToStreamingApp(userAccount)
            else:
                messagebox.showwarning('Incorrect Code', 'This code is not correct')

            
    def Login(self, email, password):  
        #uses  account modules login function to check if account exists
        userAccount = AccMod.login(email, password)
        if userAccount != False:
            self.twoFactAuth(userAccount, email)                        
        elif not email or not password: 
            messagebox.showwarning('Details Missing', 'Please enter both email and password')
        else:
            messagebox.showwarning('Account not found', 'Please enter valid credentials')
        
    
    def _build_ui(self):
        self.grid_columnconfigure((0,1,2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        
        self.label = ctk.CTkLabel(self, text="AppName Streaming Service", text_color=ColourScheme.Text, font=("arial", 40))
        self.label.grid(row=0, column=1, padx=20, pady=30, sticky="ew")
        
        self.label = ctk.CTkLabel(self, text="Email", text_color=ColourScheme.Text, font=("arial", 20))
        self.label.grid(row=1, column=1, padx=20, pady=5, sticky="ew")
        
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Enter your email", height=30)
        self.email_entry.grid(row=2,column=1,padx=20,pady=5, sticky= "ew")
        
        self.label = ctk.CTkLabel(self, text="Password", text_color=ColourScheme.Text, font=("arial", 20))
        self.label.grid(row=3, column=1, padx=20, pady=5, sticky="ew")
        
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Enter your password", height=30)
        self.password_entry.grid(row=4, column=1, padx=20, pady=5, sticky="ew")
        
        self.login_button = ctk.CTkButton(self, text="Login", fg_color=ColourScheme.Button, hover_color=ColourScheme.ButtonHover, command=lambda: self.Login(self.email_entry.get(), self.password_entry.get()))
        self.login_button.grid(row=5, column=1, padx=40, pady=5, sticky="ew")

#page after logging into an account
# I need to fix it as it doesnt immeditatley load the updataed plan + it needs to print a TXT recpiet file
class SubscriptionManagementPage(ctk.CTkFrame):
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
        

        
class ProfilePage(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, fg_color=ColourScheme.Background, bg_color=ColourScheme.Background, **kwargs)
        self.profilesframe = None
        self._build_ui()
        self.edit_profile = False
    
    def _profile_button_pressed(self, profilename):
        if self.edit_profile:
            # enter the profile editor
            editor = ProfileEditor(self, self.master.account, profilename)
        else:
            # enter browsing page with the profile
            self.master.profile = AccMod.Profile(self.master.account, profilename)
            if self.master.profile.load_from_csv():
                self.master._change_page("BrowsingPage")
    
    def _build_profilesframe(self):
        if self.profilesframe:
            self.profilesframe.grid_forget()
            for profilewidget in self.profilesframe.winfo_children():
                profilewidget.destroy()
        
        account : AccMod.Account = self.master.account
        profilenames = account._profilenames
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
        
# used to map a string to a class idk actually this seems useless
pages : dict = {"StandardPage": StandardPage, 
                "ProfilePage": ProfilePage,
                "VideoPage": VideoPage,
                "BrowsingPage": BrowsingPage, 
                "SubscriptionManagementPage": SubscriptionManagementPage, 
                "LoginPage": LoginPage, 
                "ProfilePage": ProfilePage}

class StreamingApp(ctk.CTk):
    Title = "App"
    def __init__(self):
        super().__init__()
        self.geometry("10000x10000")
        self.title("App Name Streaming Service")
        self.currentpage: ctk.CTkFrame = None
        self.account : AccMod.Account = None
        self.profile : AccMod.Profile = None
        
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)
    
    def _change_page(self, newpage, *args, **kwargs):
        if pages.get(newpage):
            # undisplay the previous page
            if self.currentpage:
                # deletes the old page
                self.currentpage.destroy()
                
            # create a new page
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

