import redis
import json

redis_host = 'localhost'
redis_port = 6379
redis_password = 'your_redis_password'

r = redis.Redis(host=redis_host, port=redis_port, password=redis_password)


class Bot:
    def __init__(self, id, name, nickname, personality, preferences):
        self.id = id
        self.name = name
        self.nickname = nickname
        self.personality = personality
        self.preferences = preferences

bot1 = Bot(id=1, name="Bot1", nickname="BotNickname1", personality="Friendly", preferences={"language": "English", "timezone": "UTC"})
bot2 = Bot(id=2, name="Bot2", nickname="BotNickname2", personality="Professional", preferences={"language": "French", "timezone": "CET"})

bot1_data = json.dumps(bot1.__dict__)
bot2_data = json.dumps(bot2.__dict__)

r.set(bot1.id, bot1_data)
r.set(bot2.id, bot2_data)

bot_id = 1  # The ID of the bot you want to retrieve

bot_data = r.get(bot_id)
if bot_data:
    bot = Bot(**json.loads(bot_data))
    print(bot.name)  # Access the attributes of the retrieved bot
else:
    print("Bot not found")