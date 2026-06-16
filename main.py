# main file for displaying GUI components
import customtkinter as ctk
import tkinter as tk
import accountmodule as AccMod
from videomodule import movies
import pyotp
import time
import smtplib


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
    Background = "#000000"
    
    Text = "#254d11"  
    Button = "#EF8606"
    ButtonHover = "#40a3a0"

class VideoWidget(ctk.CTkFrame):
    def __init__(self, image,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = image
    
    def _build_ui(self):
        pass

class ProfileWidget(ctk.CTkFrame):
    def __init__(self, master, name, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._build_ui()
        self.name = name
    
    def _build_ui():
        pass

class ProfileEditor(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def _build_ui(self):
        pass # name, movie rating
    
class StandardPage(ctk.CTkFrame):
    """
    Parent class for pages that can be accessed when in a profile
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
    
    def _build_ui(self):
        pass

    def _apply_theme(self, theme): 
        #probably won't need this since i don't think we're adding themes
        for child in self.winfo_children():
            pass

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

class SubscriptionManagementPage(StandardPage):
    pass

class LoginPage(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, fg_color=ColourScheme.Background, bg_color=ColourScheme.Background, **kwargs)
        self._build_ui()
    
    def goToStreamingApp(self, userAccount):
        ##DOESNT WORK RIGHT NOW - WILL FIX  
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
        server.sendmail(email, receiver_email, email_message)

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

class ProfilePage(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(fg_color=ColourScheme.Background, bg_color=ColourScheme.Background, *args, **kwargs)
        self._build_ui()
        
    def _build_ui(self):
        account = self.master.account
        profiles = account._profiles
        self.grid_columnconfigure((0,1,2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        
        self.label = ctk.CTkLabel(self, text="Profile Page", text_color=ColourScheme.Text, font=("arial", 40))
        self.label.grid(row=0, column=1, padx=20, pady=30, sticky="ew")

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

