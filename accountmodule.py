# classes and functions related to accounts
# e.g. logging in, changing settings

import csv
from csvmodule import *

class Profile:
    """
    Class stored inside an Account object with watchhistory and watchlist attributes for a personal feed
    """
    def __init__(self, account, name: str, age="0", newaccount = False):
        self._account: Account = account
        self._profilename = name
        self._age = age
        self._history: list = []
        self._watchlist: list = []
        if newaccount:
            self._history = []
            self._watchlist = []
        else:
            self.load_from_csv()

    def update_details(self, newname: str, newage: str, save=False):
        """
        Update the name and age of a profile in profiles.csv and its name in accounts.csv
        """
        newname = newname.strip()
        if int(newage) <= 0:
            return "Age too young"
        if len(newname) <= 1:
            return "Name too short"
        
        if save:
            edit_row("profiles.csv", 
                 ["accountemail", "profilename"], 
                 {"accountemail" : self._account._email, "profilename": self._profilename}, 
                 {"profilename": newname, "age": newage})
        
        # update profile name in account
        self._account._profilenames[self._account._profilenames.index(self._profilename)] = newname
        if save:
            self._account.save_to_csv()
        self._profilename = newname
        self._age = newage
    
    def save_to_csv(self):
        """
        Save watchlist and watchhistory to profiles.csv
        """
        edit_row("profiles.csv", 
                 ["accountemail", "profilename"], 
                 {"accountemail" : self._account._email, "profilename": self._profilename}, 
                 {"watchhistory": "/".join(self._history),
                  "watchlist": "/".join(self._watchlist)})
                
    def load_from_csv(self):
        """
        Load in the age, watchhistory and watchlist of a profile from its profilename and accountemail
        """
        data = find_row("profiles.csv", 
                        ["accountemail", "profilename"],
                        {"accountemail": self._account._email, "profilename": self._profilename})
        
        if data:
            self._age = data["age"]
            self._history = data["watchhistory"].split("/")
            self._watchlist = data["watchlist"].split("/")
            return True
        else:
            print("profile not found")
            return False

class Account:
    """
    Account interacting with app which holds profile objects and handles payment and login
    """
    def __init__(self, email: str, password: str):
        self.name = ""
        self._email : str = email
        self._plan = ""
        self._profilenames : list[str] = []
        self._profiles: list[Profile] = []
        self._password : str = password
        
    def update_plan(self, new_plan: str): 
        #fields accountname,email,password,plan,profiles
        edit_row("accounts.csv", 
                 ["email"], 
                 {"email" : self._email}, 
                 {"plan": new_plan})
        self._plan = new_plan
        self.save_to_csv()
        
        self._plan = new_plan
    
    def create_profile(self, name: str, age: str, save=False):
        """
        Create a new profile
        """
        fields = ["accountemail", "profilename", "age", "watchhistory", "watchlist"]
        if not find_row("profiles.csv", ["accountemail", "profilename"], {"accountemail": self._email, "profilename": name}):
            if not name in self._profilenames:
                self._profilenames.append(name)
                self._profiles.append(Profile(self, name, age, True))
                
            with open("profiles.csv", mode="a", newline="") as f:
                writer = csv.DictWriter(f, fields)
                writer.writerow({
                    "accountemail": self._email,
                    "profilename": name,
                    "age": age,
                    "watchhistory": "",
                    "watchlist": ""
                })
            self.save_to_csv()
            
    def delete_profile(self, profilename: str):
        """
        Delete a profile from an account by passing in its name
        """
        for profile in self._profiles:
            if profile._profilename == profilename:
                self._profiles.remove(profile)
        
        if profilename in self._profilenames:
            delete_row("profiles.csv", ["accountemail", "profilename"],
                    {"accountemail": self._email,
                        "profilename": profilename})
            self._profilenames.remove(profilename)
            self.save_to_csv()
    
    def save_to_csv(self):
        """
        save accountname, plan and profiles
        """
        edit_row("accounts.csv", 
                 ["email", "password"], 
                 {"email" : self._email, "password": self._password}, 
                 {"accountname": self.name, "plan": self._plan, "profiles": "/".join(self._profilenames)})
    
    def load_from_csv(self):
        """
        load in name, plan, profilenames from email and password
        """
        row = find_row("accounts.csv", 
                       ["email", "password"], 
                       {"email": self._email, "password": self._password})
        if row:
            self.name = row["accountname"]
            self._plan = row["plan"]
            self._profilenames = row["profiles"].split("/")
            self._profiles: list[Profile] = returnProfiles(self)
            return True
        else:
            print("account not found")
            return False

def login(email: str, password: str):
    testLogin = Account(email, password)
    if testLogin.load_from_csv():
        return testLogin
    return False

def returnProfiles(account: Account):
    """
    Get all profiles under an account
    """
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
            