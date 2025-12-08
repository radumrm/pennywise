from firebase_setup import get_database
from google.cloud import firestore

db = get_database()

def add_transaction(email, amount, trans_type, category, date, card_iban, description):
    transaction_ref = db.collection("transactions").document()
    transaction_ref.set({
        "user_email": email,
        "amount": float(amount),
        "type": trans_type,
        "category": category,
        "date": date,
        "card_iban": card_iban,
        "description": description 
    })

    card_ref = db.collection("accounts").document(email).collection("cards").document(card_iban)
    card_doc = card_ref.get()
    
    if card_doc.exists:
        current_sum = float(card_doc.to_dict().get("sum", 0.0))
        
        if trans_type == "income":
            new_sum = current_sum + float(amount)
        else:
            new_sum = current_sum - float(amount)
            
        new_sum = round(new_sum, 2)
        card_ref.update({"sum": new_sum})
        return True
    return False

def get_user_transactions(email):
    transactions_ref = db.collection("transactions")
    query = transactions_ref.where("user_email", "==", email).order_by("date", direction=firestore.Query.DESCENDING)
    results = query.stream()
    
    trans_list = []
    for doc in results:
        data = doc.to_dict()
        data['id'] = doc.id
        trans_list.append(data)
        
    return trans_list

def delete_transaction(email, transaction_id):
    trans_ref = db.collection("transactions").document(transaction_id)
    trans_doc = trans_ref.get()
    
    if not trans_doc.exists:
        return False
        
    data = trans_doc.to_dict()
    
    if data.get('user_email') != email:
        return False
        
    amount = float(data.get('amount', 0.0))
    trans_type = data.get('type')
    card_iban = data.get('card_iban')
    
    card_ref = db.collection("accounts").document(email).collection("cards").document(card_iban)
    card_doc = card_ref.get()
    
    if card_doc.exists:
        current_sum = float(card_doc.to_dict().get("sum", 0.0))
        
        if trans_type == "income":
            new_sum = current_sum - amount
        else:
            new_sum = current_sum + amount
            
        new_sum = round(new_sum, 2)
        card_ref.update({"sum": new_sum})
    
    trans_ref.delete()
    return True