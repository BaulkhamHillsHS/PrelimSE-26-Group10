# simpler functions

import csv

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
