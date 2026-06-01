# main file for displaying GUI components
import customtkinter as ctk
import tkinter as tk

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
