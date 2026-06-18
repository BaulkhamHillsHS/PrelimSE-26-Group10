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
        
def find_row(filename, fields_to_search: list, data: dict):
    for field in fields_to_search:
        if not data.get(field, False): #check if each field exists in data
            print("amount of fields must match amount of data")
            return False
    
    result_row = False
    if filename == "profiles.csv":
        f = open("profiles.csv", mode="r", newline="")
            
    elif filename == "accounts.csv":
        f = open("accounts.csv", mode="r", newline="")
    
    else:
        print("Invalid file name")
        return False
        
    reader = csv.DictReader(f)
    
    for row in reader: #for every row in the file
        found_row = True
        
        for field in fields_to_search: #for every field
            
            if row[field] != str(data[field]): #if the data does not match do not copy over
                found_row = False

        if found_row:
            result_row = row.copy() #update result_row
            break
    
    f.close() # close file after finishing
        
    return result_row

def edit_row(filename, fields_to_search: list, data: dict, newdata: dict):
    if filename == "profiles.csv":
        f = open("profiles.csv", mode="r+", newline="")
        fieldnames = ["accountemail", "profilename", "age", "watchhistory"]
    elif filename == "accounts.csv":
        f = open("accounts.csv", mode="r+", newline="")
        fieldnames = ["accountname", "email", "password", "plan", "profiles"]
    else:
        print("Invalid file name")
        return False
    
    reader = csv.DictReader(f)
    filedata = []
    for row in reader: #copy the file into a list
        found_row = True
        for field in fields_to_search:
            
            if row[field] != str(data[field]):
                found_row = False
                
        if found_row: #append edited row
            new_row = row.copy()
            for field in newdata:
                new_row[field] = str(newdata[field])
                
            filedata.append(new_row)
        
        else: #append as normal
            filedata.append(row)
    
    
    writer = csv.DictWriter(f, fieldnames)
    writer.writeheader()
    writer.writerows(filedata)
    f.close()

def delete_row(filename, fields_to_search: list, data: dict):
    if filename == "profiles.csv":
        f = open("profiles.csv", mode="r+", newline="")
        fieldnames = ["accountemail", "profilename", "age", "watchhistory"]
    elif filename == "accounts.csv":
        f = open("accounts.csv", mode="r+", newline="")
        fieldnames = ["accountname", "email", "password", "plan", "profiles"]
    else:
        print("Invalid file name")
        return False
    
    reader = csv.DictReader(f)
    filedata = []
    for row in reader: #copy the file into a list
        found_row = True
        for field in fields_to_search:
            
            if row[field] != str(data[field]):
                found_row = False
                
        if not found_row: #append non-deleted row
            filedata.append(row)
    
    writer = csv.DictWriter(f, fieldnames)
    writer.writeheader()
    writer.writerows(filedata)
    f.close()

def append_row(filename, data: dict):
    if filename == "profiles.csv":
        f = open("profiles.csv", mode="a", newline="")
        fieldnames = ["accountemail", "profilename", "age", "watchhistory"]
    elif filename == "accounts.csv":
        f = open("accounts.csv", mode="a", newline="")
        fieldnames = ["accountname", "email", "password", "plan", "profiles"]
    else:
        print("Invalid file name")
        return False
    
    writer = csv.DictWriter(f, fieldnames)
    writer.writerow(data)
    
    f.close()

delete_row("profiles.csv", ["accountemail"], {"accountemail": "tgvbhjj2@gmail.com"})

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
        if newage <= 0:
            return "Age too young"
        if len(newname) <= 1:
            return "Name too short"
        
        edit_row("accounts.csv", 
                 ["accountemail", "profilename"], 
                 {"accountemail" : self._account._email, "profilename": self._profilename}, 
                 {"profilename": newname, "age": newage})
        self._profilename = newname
        self._age = newage
    
    def save_to_csv(self):
        edit_row("accounts.csv", 
                 ["accountemail", "profilename"], 
                 {"accountemail" : self._account._email, "profilename": self._profilename}, 
                 {"watchhistory": "/".join(self._history)})
                
    def load_from_csv(self):
        data = find_row("profiles.csv", 
                        ["accountemail", "profilename"],
                        {"accountemail": self._account._email, "profilename": self._profilename})
        if data:
            self.age = data["age"]
            self.watchhistory = data["watchhistory"].split("/")
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
        fields = ["accountemail", "profilename", "age", "watchhistory"]
        if name in self._profilenames:
            with open("profiles.csv", mode="a", newline="") as f:
                writer = csv.DictWriter(f, fields)
                writer.writerow({
                    "accountemail": self._email,
                    "profilename": name,
                    "age": age
                })
            
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

testing = False
if __name__ == "__main__" and testing:
    print(login("ryan.dunne9@det.nsw.edu.au", "Baulko11!!"))
    
    my = login("ryan.dunne9@det.nsw.edu.au", "Baulko11!!")
    prof = Profile(my, "profileone")
    prof._history = ["abcd", "123"]
    prof.save_to_csv()
            