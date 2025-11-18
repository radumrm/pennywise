from firebase_setup import get_database
from google.cloud.firestore_v1 import ArrayUnion
from db_user import hash

db = get_database()


def create_card(email, IBAN, bank, card_holder_name, initial_sum, PIN):
    card_ref = db.collection("cards").document(IBAN)

    if card_ref.get().exists == True:
        card_ref.update({
            "owners" : ArrayUnion([email])
        })
        return True
    
    card_ref.set({
        "owners" : ArrayUnion([email]),
        "IBAN" : IBAN,
        "bank" : bank,
        "card_holder_name" : card_holder_name,
        "sum" : initial_sum,
        "PIN" : hash(PIN)
    })
    return True


def get_data(IBAN, PIN):
    card_snapshot = db.collection("cards").document(IBAN).get()

    if card_snapshot.exists == False:
        print("This card doesn't exist")
        return None
    
    data = card_snapshot.to_dict()
    if data["PIN"] != hash(PIN):
        print("Invalid PIN")
        return None

    return data 





    

