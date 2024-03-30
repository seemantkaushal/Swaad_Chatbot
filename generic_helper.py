
import re
def extract_session_id(session_str:str):
    match = re.search(r"projects\/.*\/agent\/sessions\/([a-zA-Z0-9-]+)\/contexts", session_str)

    if match:
        session_id = match.group(1)
        return session_id

def str_from_food_dict(food_dict:dict):
    return ", ".join([f"{int(value)} {key}" for key , value in food_dict.items()])

