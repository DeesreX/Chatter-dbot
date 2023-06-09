import redis
import json
import os
from dotenv import load_dotenv

load_dotenv("./.env")
r = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), password=os.getenv("REDIS_PASSWORD"))

class GPTBot:
    def __init__(self, id, name, nickname, personality, preferences):
        self.id = id
        self.name = name
        self.nickname = nickname
        self.personality = personality
        self.preferences = preferences
        self.memory = []

    def save_memory(self):
        memory_key = f"{self.id}:memory"
        memory_data = json.dumps(self.memory)
        r.set(memory_key, memory_data)
        print("Memory saved successfully.")

    def load_memory(self):
        memory_key = f"{self.id}:memory"
        memory_data = r.get(memory_key)
        if memory_data:
            self.memory = json.loads(memory_data)
            print("Memory loaded successfully.")
        else:
            print("No memory found.")

    def add_memory(self, memory_entry):
        self.memory.append(memory_entry)

    def get_memory(self):
        return self.memory

newBot = GPTBot(0, "Luthor", "Lucy", "Friendly", "Nice people")
newBot.add_memory('I am superman')
print(newBot.save_memory())
print(newBot.load_memory())
print(newBot.get_memory())