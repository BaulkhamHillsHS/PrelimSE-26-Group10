# simpler functions

import csv

def find_row(filename:str, fields_to_search: list[str], data: dict):
    """
    Valid filenames: profiles.csv, accounts.csv, moviesdb.csv, shows.csv, episodes.csv
    Finds and returns the data of a row in a file\n
    fields_to_search is the fields you are searching for
    data is the information for each of those fields used to determine the row
    """
    for field in fields_to_search:
        if not data.get(field, False): #check if each field exists in data
            print("amount of fields must match amount of data")
            return False
    
    result_row = False
    if filename == "profiles.csv":
        f = open("profiles.csv", mode="r", newline="")
            
    elif filename == "accounts.csv":
        f = open("accounts.csv", mode="r", newline="")
    
    elif filename == "moviesdb.csv":
        f = open("moviesdb.csv", mode="r", newline="")
    
    elif filename == "shows.csv":
        f = open("shows.csv", mode="r", newline="")
    
    elif filename == "episodes.csv":
        f = open("episodes.csv", mode="r", newline="")
    
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

def edit_row(filename:str, fields_to_search: list[str], data: dict, newdata: dict):
    """
    Valid filenames: profiles.csv, accounts.csv
    edit the data of a row in a file\n
    fields_to_search is the fields you are searching for
    data is the information for each of those fields used to determine the row
    newdata is the replacement values 
    e.g. {key_to_be_replaced : value_to_be_replaced} (does not have to replace all keys)
    """
    if filename == "profiles.csv":
        readf = open("profiles.csv", mode="r", newline="")
    elif filename == "accounts.csv":
        readf = open("accounts.csv", mode="r", newline="")
    else:
        print("Invalid file name")
        return False
    
    reader = csv.DictReader(readf)
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
    
    readf.close()
    
    if filename == "profiles.csv":
        writef = open("profiles.csv", mode="w", newline="")
        fieldnames = ["accountemail", "profilename", "age", "watchhistory", "watchlist"]
    elif filename == "accounts.csv":
        writef = open("accounts.csv", mode="w", newline="")
        fieldnames = ["accountname", "email", "password", "plan", "paymentinfo", "profiles"]
    
    writer = csv.DictWriter(writef, fieldnames)
    writer.writeheader()
    writer.writerows(filedata)
    writef.close()

def delete_row(filename:str, fields_to_search: list[str], data: dict):
    """
    Valid filenames: profiles.csv, accounts.csv
    Delete a row in a file\n
    fields_to_search is the fields you are searching for
    data is the information for each of those fields used to determine the row
    """
    if filename == "profiles.csv":
        readf = open("profiles.csv", mode="r", newline="")
    elif filename == "accounts.csv":
        readf = open("accounts.csv", mode="r", newline="")
    else:
        print("Invalid file name")
        return False
    
    reader = csv.DictReader(readf)
    filedata = []
    for row in reader: #copy the file into a list
        found_row = True
        for field in fields_to_search:
            
            if row[field] != str(data[field]):
                found_row = False
                
        if not found_row: #append non-deleted row
            filedata.append(row)
    
    readf.close()
    
    if filename == "profiles.csv":
        writef = open("profiles.csv", mode="w", newline="")
        fieldnames = ["accountemail", "profilename", "age", "watchhistory", "paymentinfo", "watchlist"]
    elif filename == "accounts.csv":
        writef = open("accounts.csv", mode="w", newline="")
        fieldnames = ["accountname", "email", "password", "plan", "profiles"]
    
    writer = csv.DictWriter(writef, fieldnames)
    writer.writeheader()
    writer.writerows(filedata)
    writef.close()

def append_row(filename:str, data: dict):
    """
    Valid filenames: profiles.csv, accounts.csv
    Add a new row at the end of a file\n
    data is the information for each of those fields used to determine the row
    """
    if filename == "profiles.csv":
        f = open("profiles.csv", mode="a", newline="")
        fieldnames = ["accountemail", "profilename", "age", "watchhistory", "watchlist"]
    elif filename == "accounts.csv":
        f = open("accounts.csv", mode="a", newline="")
        fieldnames = ["accountname", "email", "password", "plan", "paymentinfo", "profiles"]
    else:
        print("Invalid file name")
        return False
    
    writer = csv.DictWriter(f, fieldnames)
    writer.writerow(data)
    
    f.close()

def get_all_rows(filename:str):
    """
    Valid filenames: profiles.csv, accounts.csv, moviesdb.csv, shows.csv, episodes.csv
    Get all rows in a file in a list\n
    """
    if filename == "profiles.csv":
        f = open("profiles.csv", mode="r", newline="")
            
    elif filename == "accounts.csv":
        f = open("accounts.csv", mode="r", newline="")
    
    elif filename == "moviesdb.csv":
        f = open("moviesdb.csv", mode="r", newline="")
    
    elif filename == "shows.csv":
        f = open("shows.csv", mode="r", newline="")
    
    elif filename == "episodes.csv":
        f = open("episodes.csv", mode="r", newline="")
    
    else:
        print("Invalid file name")
        return False
    
    data = []
    reader = csv.DictReader(f)
    for row in reader:
        data.append(row)
    
    f.close()
    return data