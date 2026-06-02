# main file for displaying GUI components
import customtkinter as ctk
import tkinter as tk

class FontSize: 
    # so that we can easily change formatting
    # use variables (like FontSize.Title) instead of 16
    Title = 16
    """16"""
    Subtitle = 14
    """14"""
    Text = 11
    """11"""

class SettingsPage(ctk.CTkFrame):
    pass

class VideoPage(ctk.CTkFrame):
    """
    Screen to display when selecting a movie/show
    """
    def __init__(self):
        super().__init__()
    
    def _build_ui(self):
        pass

class LoginPage(ctk.CTkFrame):
    def __init__():
        pass
    
    def _build_ui():
        pass

class SignUpPage(ctk.CTkFrame):
    pass

class PaymentPlanPage(ctk.CTkFrame):
    pass

class StreamingApp(ctk.CTk):
    Title = "App"
    def __init__(self):
        super().__init__()
        self.pages = []
        self.currentpage = None
        self.account = None
        self.profile = None
    
    def _change_page(self):
        pass
        
if __name__ == "__main__":
    app = StreamingApp()
    app.mainloop()
