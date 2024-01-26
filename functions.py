class Command:
    def __init__(self, content: str, author: str, id, args: list):
        self.content = content
        self.author = author
        self.id = id
        self.args = args

class Selfbot:
    def __init__(self, TOKEN, CHANNEL, PREFIX):
        self.TOKEN = TOKEN
        self.CHANNEL = CHANNEL
        self.PREFIX = PREFIX

    def get_username(self, get_id=False):
        import requests, json

        head = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            'Authorization': self.TOKEN
        }
        try:
            r = requests.get(f"https://discord.com/api/v9/users/@me", headers=head)
            response = json.loads(r.text)
            username = response['username']
        except:
            return 1
        
        
        
        if get_id == False: return username
        elif get_id == True:
            id = response['id']
            return username, id

    def get_last_message(self, channel_id, get_message_id=False):
        import requests, json

        head = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            'Authorization': self.TOKEN
        }
        try:
            r = requests.get(f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=1", headers=head)
            response = json.loads(r.text)
            content = response[0]['content']
        
            author_name = response[0]['author']['username']
        except:
            return 1
        
        if get_message_id == False: return content, author_name
        elif get_message_id == True:
            id = response[0]['id']
            return content, author_name, id
        
    def send_message(self, text, channel_id, get_massage_id=False):
        import requests
        import json

        head = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            'Authorization': self.TOKEN
        }

        try:
            r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=head, json={'content': text})
            response = json.loads(r.text)
        except: return 1

        
        if get_massage_id == True:
            id = response['id']
            return id

    def delete_message(self, message_id, channel_id):
        import requests

        head = { 
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            'Authorization': self.TOKEN
        }

        try:
            r = requests.delete(f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}", headers=head)
        except: return 1

    def edit_message(self, new_text, message_id, channel_id):
        import requests

        head = { 
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            'Authorization': self.TOKEN
        }

        data = {
            'content': new_text
        }

        try:
            r = requests.patch(f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}", headers=head, json=data)
        except: return 1 

    def command(self, command_name):
        def decorator(func):
            content, author, id = self.get_last_message(self.CHANNEL, get_message_id=True)
            username = self.get_username()

            args = content.split(" ")[1:]
            
            if content.startswith(self.PREFIX+command_name) and author == username:
                func(Selfbot(self.TOKEN, self.CHANNEL, self.PREFIX), Command(content, author, id, args))

        return decorator

        
# Broken
def get_token(username, password):
    import requests
    import json

    head = { "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" }
    jsonn = {
        "login": username,
        "password": password
    }
    try:
        r = requests.post("https://discord.com/api/v9/auth/login", headers=head, json=jsonn).text
        response = json.loads(r)
        return response['token']
    except Exception as e:
        print(e)
        return 1    
