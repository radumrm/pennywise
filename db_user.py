import hashlib
from firebase_setup import get_database

def create_account(email, name, password):
    db = get_database()

    doc_snapshot = db.collection("accounts").document(email).get()
    if doc_snapshot.exists == True:
        print("Email already registered")
        return False

    password_bytes = password.encode('utf-8')
    password_hash = hashlib.sha256(password_bytes).hexdigest()

    doc_ref = db.collection("accounts").document(email)
    doc_ref.set({
        "email" : email,
        "name" : name,
        "password" : password_hash
    })
    return True


def delete_account(email, password):
    db = get_database()

    accounts_ref = db.collection("accounts")
    docs = accounts_ref.stream()

    doc_snapshot = db.collection("accounts").document(email).get()
    if doc_snapshot.exists == False:
        print("Account doesn't exist")
        return False
    
    password_bytes = password.encode('utf-8')
    password_hash = hashlib.sha256(password_bytes).hexdigest()
    
    doc_ref = db.collection("accounts").document(email)
    data = doc_ref.get().to_dict()
    if data["password"] != password_hash:
        print("Invalid password")
        return False

    doc_ref.delete()
    return True


def login(email, password):
    db = get_database()

    doc_snapshot = db.collection("accounts").document(email).get()
    if doc_snapshot.exists == False:
        print("Account doesn't exist")
        return None

    password_bytes = password.encode('utf-8')
    password_hash = hashlib.sha256(password_bytes).hexdigest()

    data = doc_snapshot.to_dict()
    if data["password"] != password_hash:
        print("Invalid password")
        return None
    
    return data

def change_name(email, password, new_name):
    db = get_database()

    doc_snapshot = db.collection("accounts").document(email).get()
    if doc_snapshot.exists == False:
        print("Account doesn't exist")
        return False
    
    password_bytes = password.encode('utf-8')
    password_hash = hashlib.sha256(password_bytes).hexdigest()

    data = doc_snapshot.to_dict()
    if data["password"] != password_hash:
        print("Invalid password")
        return False
    
    db.collection("accounts").document(email).set({
        "email" : email,
        "name" : new_name,
        "password" : password_hash
    })
    return True


def change_password(email, password, new_password):
    db = get_database()

    doc_snapshot = db.collection("accounts").document(email).get()
    if doc_snapshot.exists == False:
        print("Account doesn't exist")
        return False
    
    password_bytes = password.encode('utf-8')
    password_hash = hashlib.sha256(password_bytes).hexdigest()

    data = doc_snapshot.to_dict()
    if data["password"] != password_hash:
        print("Invalid password")
        return False
    
    new_password_bytes = new_password.encode('utf-8')
    new_password_hash = hashlib.sha256(new_password_bytes).hexdigest()

    db.collection("accounts").document(email).set({
        "email" : email,
        "name" : data["name"],
        "password" : new_password_hash
    })
    return True
    



