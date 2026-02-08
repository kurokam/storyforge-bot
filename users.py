users = {}

def inc_use(user_id):
    users.setdefault(user_id, {"count": 0})
    users[user_id]["count"] += 1
    return users[user_id]["count"]
