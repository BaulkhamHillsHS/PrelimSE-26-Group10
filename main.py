# main file for displaying GUI components
import customtkinter as ctk
import tkinter as tk
import accountmodule as AccMod
from videomodule import movies
import pyotp
import time
import smtplib
from PIL import Image #used for profile images

class Font:
    Title = ""
    Subtitle = ""
    Text = ""

class FontSize: 
    # so that we can easily change formatting
    # use variables (like FontSize.Title) instead of 16
    Title = 16
    """16"""
    Subtitle = 14
    """14"""
    Text = 11
    """11"""

class ColourScheme: # for colours that won't change throughout whole app
    #temporary (looks very bad)
    Primary = "#2d8a1f"
    Secondary = "#dee60e"
    Foreground = "#557c45"
    Background = "#FDD973"
    
    Text = "#1e3712"  
    Button = "#EF8606"
    ButtonHover = "#40a3a0"

# widgets
class VideoWidget(ctk.CTkFrame):
    def __init__(self, image,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = image
    
    def _build_ui(self):
        pass

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
class ProfileEditor(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.focus()
    
    def _build_ui(self):
        pass # name, movie rating

#pages    
class StandardPage(ctk.CTkFrame):
    """
    Parent class for pages that can be accessed when in a profile
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
    
    def _build_ui(self): #method to be overriden
        pass

#pages after picking a profile
class VideoPage(StandardPage):
    """
    Screen to display when selecting a movie/show
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def _build_ui(self):
        m_rom1_img = self.insertVideo(movies[0], 200, 200)
        self.m_rom1_icon = ctk.CTkLabel(self.login_frame,text="",image=m_rom1_img)
        self.m_rom1_icon.pack(padx=0,pady=30)
    
    def insertVideo(self, raw_image, width, height ):
        #practice import of an image       
        m_raw = raw_image
        m_img = ctk.CTkImage(
            light_image=m_raw.thumbnail,
            dark_image=m_raw.thumbnail,
            size=(width, height)
        )
        return m_img
        
class BrowsingPage(StandardPage):
    pass

#starting page    
class LoginPage(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, fg_color=ColourScheme.Background, bg_color=ColourScheme.Background, **kwargs)
        self._build_ui()
    
    def goToStreamingApp(self, userAccount):
        ##DOESNT WORK RIGHT NOW - WILL FIX  
        #idk it seems pretty working to me
        self.master.account = userAccount
        app._change_page("ProfilePage")
        
    
    def twoFactAuth(self, userAccount, user_email):
        
        for widget in self.winfo_children():
                widget.destroy()   
        self.grid_columnconfigure((0,1,2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        
        #build page elements
        self.label = ctk.CTkLabel(self, text="AppName Streaming Service", text_color=ColourScheme.Text, font=("arial", 40))
        self.label.grid(row=0, column=1, padx=20, pady=30, sticky="ew")
            
        self.label = ctk.CTkLabel(self, text="A six digit code has been sent to your email: ", text_color=ColourScheme.Text, font=("arial", 20))
        self.label.grid(row=1, column=1, padx=20, pady=5, sticky="ew")
        
        self.code_entry = ctk.CTkEntry(self, placeholder_text="XXXXXX", height=30)
        self.code_entry.grid(row=2, column=1, padx=20, pady=5, sticky="ew")
    
        self.submit_button = ctk.CTkButton(self, text="Submit", fg_color=ColourScheme.Button, hover_color=ColourScheme.ButtonHover, command= lambda: checkUsercode(self.code_entry.get(), code))
        self.submit_button.grid(row=3, column=1, padx=40, pady=5, sticky="ew")

        #send email
        email = "devashreepatel95@gmail.com" #usually company email
        receiver_email = user_email
        code = str(123456)
        email_message = f"Subject: APPNAME STREAMING SERVICE SIX-DIGIT CODE \n\n Your one time six digit code is: {code} This code expires in 15 minutes."
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email,"luruzlexucsjtmjg")
        # the line below is temporarily disabled as I do not want to send 5 million emails
        # to random accounts while testing out other functions!
        #server.sendmail(email, receiver_email, email_message)

        def checkUsercode(usercode, code):    
            if usercode == code:
                self.goToStreamingApp(userAccount)

            
    def Login(self, email, password):  
        #uses  account modules login function to check if account exists
        userAccount = AccMod.login(email, password)
        if userAccount != False:
            self.twoFactAuth(userAccount, email)                        
        else:
            print("Incorrect email or password")
        
    
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
class SubscriptionManagementPage(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, fg_color=ColourScheme.Background, bg_color=ColourScheme.Background, **kwargs)
        self._build_ui()
    def _build_ui(self):
        self.grid_columnconfigure((0,1,2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        
        self.label = ctk.CTkLabel(self, text="Manage Subscription", text_color=ColourScheme.Text, font=("arial", 40))
        self.label.grid(row=0, column=1, padx=20, pady=30, sticky="ew")
        
        def button_event():
            app._change_page("ProfilePage")

        self.return_button = ctk.CTkButton(app, text="Return to Profiles", command=button_event)
        self.return_button.grid(row=0, column=2, padx=20, pady=30, sticky="nw")

        account_plan = "Current Account Plan: premium"
        self.current_acc_plan = ctk.CTkLabel(self, text=account_plan, text_color=ColourScheme.Text, font=("arial", 20))
        self.current_acc_plan.grid(row=2, column=1, padx=20, pady=30, sticky="ew")

class ProfilePage(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(fg_color=ColourScheme.Background, bg_color=ColourScheme.Background, *args, **kwargs)
        self._build_ui()
        self.edit_profile = False
    
    def _profile_button_pressed(self, profilename):
        if self.edit_profile:
            # enter the profile editor
            pass
        else:
            # enter browsing page with the profile
            pass
    
    def _build_profilesframe(self):
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
    
    def _build_ui(self):
        self.grid_columnconfigure((0,1,2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self._build_profilesframe()
        self.profilesframe.grid(column=1,row=2)
        
        self.label = ctk.CTkLabel(self, text="Profile Page", text_color=ColourScheme.Text, font=("arial", 40))
        self.label.grid(row=0, column=1, padx=20, pady=30, sticky="ew")
        
        def manageSub():
            app._change_page("SubscriptionManagementPage")

        self.sub_man_button = ctk.CTkButton(self, text="Manage Subscription", command=manageSub)
        self.sub_man_button.grid(row=5, column=0, padx=20, pady=30, sticky="se")

        def logOut():
            app._change_page("LoginPage")
        
        self.log_out_button = ctk.CTkButton(self, text="Log Out", fg_color="red", command=logOut)
        self.log_out_button.grid(row=5, column=2, padx=20, pady=30, sticky="sw")

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
        self.currentpage: ctk.CTkFrame = None
        self.account : AccMod.Account = None
        self.profile : AccMod.Profile = None
        
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)
    
    def _change_page(self, newpage):
        if pages.get(newpage):
            # undisplay the previous page
            if self.currentpage:
                # deletes the old page
                self.currentpage.destroy()
                
            # create a new page
            self.currentpage = pages[newpage](self)
            
            # display the new page
            self.currentpage.grid(row=0, column=0, sticky="nesw")
        else:
            raise KeyError(f"Page {newpage} does not exist")
    
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
    app._test_page(LoginPage(app))
    app.mainloop()

