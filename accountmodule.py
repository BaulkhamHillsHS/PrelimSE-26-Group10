# classes and functions related to accounts
# e.g. logging in, changing settings

import csv
from csvmodule import *

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
        self._history: list = []
        self._theme = Theme()
        self.load_from_csv()

    def update_details(self, newname, newage):
        newname = newname.strip()
        if int(newage) <= 0:
            return "Age too young"
        if len(newname) <= 1:
            return "Name too short"
        
        edit_row("profiles.csv", 
                 ["accountemail", "profilename"], 
                 {"accountemail" : self._account._email, "profilename": self._profilename}, 
                 {"profilename": newname, "age": newage})
        self._account._profilenames[self._account._profilenames.index(self._profilename)] = newname
        self._account.save_to_csv()
        self._profilename = newname
        self._age = newage
    
    def save_to_csv(self):
        edit_row("profiles.csv", 
                 ["accountemail", "profilename"], 
                 {"accountemail" : self._account._email, "profilename": self._profilename}, 
                 {"watchhistory": "/".join(self._history)})
                
    def load_from_csv(self):
        data = find_row("profiles.csv", 
                        ["accountemail", "profilename"],
                        {"accountemail": self._account._email, "profilename": self._profilename})
        if data:
            self._age = data["age"]
            self._history = data["watchhistory"].split("/")
            return True
        else:
            print("profile not found")
            return False

class Account:
    def __init__(self, email, password):
        self.name = ""
        self._email : str = email
        self._plan = ""
        self._profilenames : list[Profile] = []
        self._password : str = password
        
    def create_profile(self, name, age):
        # not bothered to rewrite it with csvmodule
        fields = ["accountemail", "profilename", "age", "watchhistory"]
        if not find_row("profiles.csv", ["accountemail", "profilename"], {"accountemail": self._email, "profilename": name}):
            if not name in self._profilenames:
                self._profilenames.append(name)
            with open("profiles.csv", mode="a", newline="") as f:
                writer = csv.DictWriter(f, fields)
                writer.writerow({
                    "accountemail": self._email,
                    "profilename": name,
                    "age": age,
                    "watchhistory": ""
                })
            self.save_to_csv()
            
    def delete_profile(self, profilename):
        if profilename in self._profilenames:
            delete_row("profiles.csv", ["accountemail", "profilename"],
                    {"accountemail": self._email,
                        "profilename": profilename})
            self._profilenames.remove(profilename)
            self.save_to_csv()
    
    def save_to_csv(self):
        edit_row("accounts.csv", 
                 ["email", "password"], 
                 {"email" : self._email, "password": self._password}, 
                 {"accountname": self.name, "plan": self._plan, "profiles": "/".join(self._profilenames)})
    
    def load_from_csv(self):
        row = find_row("accounts.csv", 
                       ["email", "password"], 
                       {"email": self._email, "password": self._password})
        if row:
            self.name = row["accountname"]
            self._plan = row["plan"]
            self._profilenames = row["profiles"].split("/")
            return True
        else:
            print("account not found")
            return False

def login(email, password):
    testLogin = Account(email, password)
    if testLogin.load_from_csv():
        return testLogin
    return False

def returnProfiles(account: Account):
    acc_profiles = []
    for profile  in account._profilenames:
        acc_profiles.append(Profile(account,profile))
    return acc_profiles

testing = False
if __name__ == "__main__" and testing:
    print(login("ryan.dunne9@det.nsw.edu.au", "Baulko11!!"))
    
    my = login("ryan.dunne9@det.nsw.edu.au", "Baulko11!!")
    prof = Profile(my, "profileone")
    prof._history = ["abcd", "123"]
    prof.save_to_csv()
            