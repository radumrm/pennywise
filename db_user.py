import hashlib
from firebase_setup import get_database

db = get_database()


def hash(password):
    password_bytes = password.encode('utf-8')
    hash = hashlib.sha256(password_bytes).hexdigest()
    return hash


def create_account(email, name, password):
    doc_ref = db.collection("accounts").document(email)
    if doc_ref.get().exists == True:
        print("Email already registered")
        return False

    doc_ref.set({
        "email" : email,
        "name" : name,
        "password" : hash(password)
    })
    return True


def delete_account(email, password):
    doc_ref = db.collection("accounts").document(email)
    if doc_ref.get().exists == False:
        print("Account doesn't exist")
        return False

    data = doc_ref.get().to_dict()
    if data["password"] != hash(password):
        print("Invalid password")
        return False

    doc_ref.delete()
    return True


def login(email, password):
    doc_snapshot = db.collection("accounts").document(email).get()
    if doc_snapshot.exists == False:
        print("Account doesn't exist")
        return None

    data = doc_snapshot.to_dict()
    if data["password"] != hash(password):
        print("Invalid password")
        return None

    return data


def change_name(email, password, new_name):
    doc_snapshot = db.collection("accounts").document(email).get()
    if doc_snapshot.exists == False:
        print("Account doesn't exist")
        return False

    data = doc_snapshot.to_dict()
    if data["password"] != hash(password):
        print("Invalid password")
        return False
    
    db.collection("accounts").document(email).set({
        "email" : data["email"],
        "name" : new_name,
        "password" : data["password"]
    })
    return True


def change_password(email, password, new_password):
    doc_snapshot = db.collection("accounts").document(email).get()
    if doc_snapshot.exists == False:
        print("Account doesn't exist")
        return False

    data = doc_snapshot.to_dict()
    if data["password"] != hash(password):
        print("Invalid password")
        return False
    
    db.collection("accounts").document(email).set({
        "email" : data["email"],
        "name" : data["name"],
        "password" : hash(new_password)
    })
    return True
    

def change_email(email, password, new_email):
    doc_screenshot = db.collection("accounts").document(email).get()
    if doc_screenshot.exists == False:
        print("Account doesn't exist")
        return False

    name = doc_screenshot.to_dict()["name"]
    rez_del = delete_account(email, password)
    if rez_del == False:
        return False
    
    return create_account(new_email, name, password)
    

