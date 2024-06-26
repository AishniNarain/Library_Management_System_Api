from app import client
import datetime

database = client["library"]
users_logs_collection = database["users_logs"]

def log_users_action(action, status, message, user_id=None, data=None):
    log_entry = {
        "action": action,
        "status": status,
        "message": message,
        "user_id": user_id,
        "data": data,
        "timestamp": datetime.datetime.now()
    }
    
    users_logs_collection.insert_one(log_entry)