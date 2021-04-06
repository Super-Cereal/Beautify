import requests


def req(req_type, url):
    base_url = "http://127.0.0.1:5000/api/v1.0"
    if req_type == "get":
        res = requests.get(f'{base_url}/{url}')
    elif req_type == "post":
        res = requests.post(f'{base_url}/{url}')
    elif req_type == "delete":
        res = requests.delete(f'{base_url}/{url}')
    print(res.json())
    # print(res.text)


req("get", "auth")
req("post", "users?password=1234&email=asatru@mail.com&nickname=vovan")
req("post", "auth?password=1234&email=asatru@mail.com&remember_me=True")
req("get", "auth")
