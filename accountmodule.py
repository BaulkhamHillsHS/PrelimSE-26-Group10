# classes and functions related to accounts
# e.g. logging in, changing settings
class Theme:
    """
    Colour theme of the app
    """
    def __init__(self):
        pass
    
class Profile:
    def __init__(self):
        self._history = []
        self._theme = Theme()

class Account:
    def __init__(self):
        self._email = None
        self._plan = None
        self._profiles = []
        self._password = None
    
    def save_to_csv(self):
        pass