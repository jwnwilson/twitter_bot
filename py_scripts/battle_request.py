import requests
import json

def battle_request(id):
    """
    create a POST request for battle results via our very limited 'API'
    :param id: battle id to retrieve data for
    :return: json string
    """
    post_data = {"id":id}
    battle_data = requests.post("http://localhost:8000/hash_tag_battle/", data=post_data)
    return battle_data.text

if __name__ == "__main__":
    print battle_request(1)
