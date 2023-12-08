import os
import pymongo
if os.path.exists("env.py"):
    import env

MONGO_URI = os.environ.get("MONGO_URI")
DATABASE = "myFirstDB"
COLLECTION = "celebrities"


def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s") % e

def show_menu():
    print("")
    print("1. Add a record")
    print("2. Find a record")
    print("3. Edit a record")
    print("4. Delete a record")
    print("5. Exit")

    option = input("Enter option: ")
    return option



def get_record():
    print("")
    first = input("Enter first Name >")
    last = input("Enter last Name >") 

    try:
        doc = coll.find_one({"first" : first.lower(), "last" : last.lower()})
    except:
        print("Error accessing the database")

    if not doc:
        print("")
        print("Error! No results found.")
    
    return doc


def add_record():
    print("")
    first = input("Enter first Name >")
    last = input("Enter last Name >")
    dob = input("Enter Date of Birth >")
    gender = input("Enter Gender >")
    hair_color = input("Enter Hair Color >")
    occupation = input("Enter occupation >")
    nationality = input("Enter nationality >")

    new_doc = {
        "first" : first.lower(),
        "last" : last.lower(),
        "dob" : dob,
        "gender" : gender,
        "hair_color" : hair_color,
        "occupation" : occupation.lower(),
        "nationality" : nationality.lower()
    }

    try :
        coll.insert_one(new_doc)
        print("")
        print("Document inserted")
    except:
        print("Error accessing the database")


def find_record():
    doc = get_record()
    if doc:
        print("")
        for k,v in doc.items():
            if k != "_id":
                print(k.capitalize() + ": " + v.capitalize())


def edit_record():
    doc = get_record()
    if doc:
        update_doc = {}
        print("")
        for k,v in doc.items():
            if k != "_id":
                update_doc[k] = (input((k.capitalize() + "[" + v + "] >"))).lower()

                if update_doc[k] == "":
                    update_doc[k] = v
        try:
            coll.update_one(doc, {"$set": update_doc})
            print("")
            print("Document Updated")
        except:
            print("Error accessing the database")

def delete_record():
    doc = get_record()
    if doc:
        print("")
        for k,v in doc.items():
            if k != "_id":
                print(k.capitalize() + ": " +v.capitalize())
            
        print("")
        confirmation = input("Is this the document you want to delete?\nY or N >")
        print("")

        if confirmation.lower() == "y":
            try:
                coll.delete_one(doc)
                print("Document Deleted!")
            except:
                print("Error accessing the database")
        else:
            print("Document not deleted")



def main_loop():
    while True:
        option = show_menu()
        if option == "1":
            add_record()
        elif option == "2":
            find_record()
        elif option == "3":
            edit_record()
        elif option == "4":
            delete_record()
        elif option == "5":
            conn.close()
            break
        else:
            print("Invalid option")
        print("")




conn = mongo_connect(MONGO_URI)
coll = conn[DATABASE][COLLECTION]
main_loop()