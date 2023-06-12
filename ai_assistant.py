import discord
from discord.ext import commands
import openai
import requests
from requests.structures import CaseInsensitiveDict
import json
import os
from dotenv import load_dotenv
from bots import GPTBot

SIZES = ['256x256', '512x512', '1024x1024']

load_dotenv('./.env')
openai.api_key = os.getenv('CHAT_TOKEN')

class DiscordBot:
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        self.bot = commands.Bot(command_prefix='/', description="A BOT", intents=intents)

    # Rest of the code for the DiscordBot class...

bot = DiscordBot()

@bot.bot.event
async def on_ready():
    print(f'Coding senpei has landed. Get ready!')

bot.bot.run(os.getenv("DISCORD_TOKEN"))