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

class VideoFrame(ctk.CTkFrame):
    """
    UI component to display videos (movies and tv shows)
    """
    def __init__(self):
        super().__init__()
    
    def build_ui(self):
        pass

class StreamingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
    
    def build_ui(self):
        pass
        
if __name__ == "__main__":
    app = StreamingApp()
    app.mainloop()
