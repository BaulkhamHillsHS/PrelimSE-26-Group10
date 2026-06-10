# classes and functions related to accounts
# e.g. logging in, changing settings

import csv

class Theme:
    """
    Colour theme of the app
    """
    def __init__(self): # 
        self.Primary = "#34c9c0"
        self.Secondary = "#dee60e"
        self.Foreground = "#3c807e"
        self.Background = "#000000"  
        self.Text = "#ececec" 
        self.Button = "#3b7472"
        self.ButtonHover = "#40a3a0"
        
class Profile:
    def __init__(self, account, name):
        self._account: Account = account
        self._profilename = name
        self._age = 0
        self._history = []
        self._theme = Theme()
        self.load_from_csv()

    def save_to_csv(self):
        fields = ["accountemail", "profilename", "age", "watchhistory"]
        with open("profiles.csv") as f:
            pass
    
    def load_from_csv(self):
        with open("profiles.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["accountemail"].strip() == self._account._email and row["profilename"].strip() == self._profilename:
                    self._age = row["age"]
                    self._history = row["watchhistory"].split("/")
                    break

class Account:
    def __init__(self, email, password):
        self._email = email
        self._plan = None
        self._profiles = []
        self._password = password
        
    def create_profile(self):
        pass
            
    def save_to_csv(self):
        fields = ["accountname", "email", "password", "plan", "profiles"]
    
    def load_from_csv(self):
        with open("accounts.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["email"].strip() == self._email and row["password"].strip() == self._password:
                    self._plan = row["plan"]
                    self._profiles = row["profiles"].split("/")
                return True
        return False # no account found

def login(email, password):
    testLogin = Account(email, password)
    if testLogin.load_from_csv():
        return testLogin
    return False

if __name__ == "__main__":
    print(login("ryan.dunne9@det.nsw.edu.au", "Baulko11!!"))