import json

class Config:

    def __init__(self):
        with open("config.json", "r") as f:
            self.config = json.load(f)

    def get_profile_name(self):
        return self.config['profile_name']