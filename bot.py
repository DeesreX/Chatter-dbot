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

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='/', description="A BOT", intents=intents)

# Example usage
gentle_bot = GPTBot(
    id=1,
    name="GentleBot",
    nickname="GentleOne",
    personality="Gentle",
    preferences={"language": "English", "timezone": "UTC"}
)

sensei_bot = GPTBot(
    id=0,
    name="Coding Sensei",
    nickname="Sensei",
    personality="Strict, Sensei",
    preferences={"language": "English", "timezone": "UTC"}
)

# Add some gentle memories
gentle_bot.add_memory("You are kind and compassionate.")
gentle_bot.add_memory("Spread love and positivity.")
gentle_bot.add_memory("Be gentle in your words and actions.")

# Save the bot's memory to Redis
gentle_bot.save_memory()

# Load the bot's memory from Redis
gentle_bot.load_memory()

# Print the loaded memory
print(gentle_bot.memory)


def getResponse(text, system = "", bot = GPTBot(None,None,None,None,None)):
    memories = bot.get_memory()

    messages = [
        {"role": "system", "content": system + " ".join(memories)},
        {"role": "user", "content": text},
    ]

    response = openai.ChatCompletion.create(
    model= "gpt-3.5-turbo",
    messages = messages
    )

    completion = response.choices[0]["message"]["content"]
    return completion


def getImageResponse(prompt):
    generation_size = SIZES[0]
    response = openai.Image.create(
    prompt=prompt,
    n=1,
    size=generation_size
    )
    image_url = response['data'][0]['url']
    return image_url




@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

@bot.event
async def on_message(message):
    allowed = ["DeesreX", "NO.", "Mage", "HighVoltage", "Demikas", "Codename", "LF", "CaFe MogadoR -Upland Daily News"]
    # Check if the message is sent by a user and not a bot
    if message.author.name in allowed:
        gentle_bot.add_memory(message.content)
        # check what channel
        if message.channel.name == "chat":
            await chat(message)
        elif message.channel.name == "image-generation":
            await image_generation(message)
        elif message.channel.name == "code-explained":
            task = "Explain the code"
            response = getResponse(f"{task} \n {message.content}", gentle_bot)
            response_with_mention = f"{message.author.mention} {response}"
            async with message.channel.typing():
                await message.channel.send(response_with_mention)
        elif message.channel.name == "code-questions":
            task = "You are a assistant coder. Please respond to the following: "
            response = getResponse(f"{task} \n {message.content, gentle_bot}")
            response_with_mention = f"{message.author.mention} {response}"
            async with message.channel.typing():
                await message.channel.send(response_with_mention)
        elif message.channel.name == "pre-alpha":
            task = "Coding Teacher"
            response = getResponse(message.content, task, sensei_bot)
            response_with_mention = f"{message.author.mention} {response}"
            async with message.channel.typing():
                await message.channel.send(response_with_mention)


async def image_generation(message):
    image_url = getImageResponse(message.content)
    embed = discord.Embed()
    embed.set_image(url=image_url)
    response_with_mention = f"{message.author.mention}"
    async with message.channel.typing():
        await message.channel.send(response_with_mention, embed=embed)

async def chat(message):
    async with message.channel.typing():
        user_content = "USER_MESSAGE[" + message.content + "] from (" + str(message.author) + ")"
        system_content = "YOUR MEMORIES [\n".join(gentle_bot.get_memory()) + "\n]"
        response = getResponse(user_content, system_content)
        response_with_mention = f"{message.author.mention}, {response}"
        await message.channel.send(response_with_mention)


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')

if __name__ == "__main__":
    description = '''An example bot to showcase the discord.ext.commands extension
    module.
    There are a number of utility commands being showcased here.'''
    bot.run(os.getenv("REXTOPIA_TOKEN"))

