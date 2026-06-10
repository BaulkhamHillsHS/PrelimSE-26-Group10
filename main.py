# main file for displaying GUI components
import csv
import customtkinter as ctk
import tkinter as tk
import accountmodule as Account
from videomodule import movies
import pyotp
import time

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
    Primary = "#34c9c0"
    Secondary = "#dee60e"
    Foreground = "#3c807e"
    Background = "#000000"
    Text = "#ececec"  
    Button = "#3b7472"
    ButtonHover = "#40a3a0"

class VideoWidget(ctk.CTkFrame):
    def __init__(self, image,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = image
    
    def _build_ui(self):
        pass


class StandardPage(ctk.CTkFrame):
    """
    Parent class for pages that can be accessed when in a profile
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
    
    def _build_ui(self):
        pass

    def _apply_theme(self, theme):
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
        
        

class SubscriptionManagementPage(StandardPage):
    pass

class LoginPage(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(fg_color=ColourScheme.Background, bg_color=ColourScheme.Background, *args, **kwargs)
        
        self._build_ui()

    def Login(self, email, password):
        
        key = pyotp.random_base32()
        self.totp = pyotp.TOTP(key)
        print(self.totp.now())
        
        if email == "devashreepatel95@gmail.com" and password == "abc123":        
            input_code = input("Enter 2FA Code: ")
            self.totp.verify(input_code)
                         
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
       
        
        

class PaymentPlanPage(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def _build_ui(self):
        pass

class StreamingApp(ctk.CTk):
    Title = "App"
    def __init__(self):
        super().__init__()
        self.pages = {}
        self.currentpage: ctk.CTkFrame = None
        self.account = None
        self.profile = None
        
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)
    
    def _change_page(self, newpage):
        if self.currentpage:
            self.currentpage.grid_forget()
        self.currentpage = self.pages[newpage]
        self.currentpage.grid(row=0, column=0, sticky="nesw")
    
    def _test_page(self, page):
        """
        See what a page looks like (for testing only)
        """
        if self.currentpage:
           self.currentpage.grid_forget()
        self.currentpage = page
        self.currentpage.grid(row=0, column=0, sticky="nesw")
        

        
if __name__ == "__main__":
    app = StreamingApp()
    app._test_page(LoginPage(app))
    app.mainloop()

