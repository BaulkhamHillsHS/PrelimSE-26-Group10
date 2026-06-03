# main file for displaying GUI components
import customtkinter as ctk
import tkinter as tk
import accountmodule as Account
import videomodule as Video

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
    Button = "#3b7472"
    ButtonHover = "#40a3a0"

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

class SettingsPage(StandardPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def _build_ui(self):
        pass

class VideoPage(StandardPage):
    """
    Screen to display when selecting a movie/show
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def _build_ui(self):
        pass

class SubscriptionManagementPage(StandardPage):
    pass

class LoginPage(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(fg_color=ColourScheme.Background, bg_color=ColourScheme.Background, *args, **kwargs)
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)
        self._build_ui()
    
    def _build_ui(self):
        self.login_frame = ctk.CTkFrame(self, fg_color=ColourScheme.Foreground)
        self.login_frame.grid(row=0, column=0, ipadx=100, ipady=0)
        
        self.text = ctk.CTkLabel(self.login_frame, text="Login Page")
        self.text.pack(padx=0,pady=30)
        
        self.email_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Enter your email")
        self.email_entry.pack(padx=0,pady=20)
        
        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Enter your password")
        self.password_entry.pack(padx=0,pady=20)
        
        self.login_button = ctk.CTkButton(self.login_frame, text="Login", fg_color=ColourScheme.Button, hover_color=ColourScheme.ButtonHover)
        self.login_button.pack(padx=0,pady=30)

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
