# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands
import openai
import requests
from requests.structures import CaseInsensitiveDict
import json
import os
from dotenv import get_variables




# import client

# history = []

# @client.command()
# @commands.check(lambda ctx: ctx.channel.name == "code-questions")
# async def get_history(ctx):
#     response_with_mention = f"{ctx.author.mention}, here is your history list:\n"
#     for response in history:
#         response_with_mention += response + "\n"
#     async with ctx.typing():
#         await ctx.send(response_with_mention)

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)
history = []
# Set up your OpenAI API credentials
openai.api_key = get_variables('./.env')['CHAT_TOKEN']
tosend = {
  "model": "gpt-3.5-turbo",
  "messages": [{"role": "user", "content": "Hello!"}]
}

def getResponse(text):
    response = openai.ChatCompletion.create(
    model= "gpt-3.5-turbo",
    messages= [{"role": "user", "content": text}]
    )
    # Get the generated text from the API response
    completion = response.choices[0]["message"]["content"]
    return completion


def getImageResponse(prompt):
    response = openai.Image.create(
    prompt=prompt,
    n=1,
    size="256x256"
    )
    image_url = response['data'][0]['url']
    return image_url




@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

@bot.event
async def on_message(message):
    allowed = ["DeesreX", "NO.", "Mage", "HighVoltage", "Demikas"]
    # Check if the message is sent by a user and not a bot
    async with message.channel.typing():
        if message.author.name in allowed:
            # check what channel
            if message.channel.name == "chat":
                await chat(message)
            elif message.channel.name == "image-generation":
                await image_generation(message)


            elif message.channel.name == "code-explained":
                task = "Explain the code"
                response = getResponse(f"{task} \n {message.content}")
                response_with_mention = f"{message.author.mention} {response}"
                async with message.channel.typing():
                    await message.channel.send(response_with_mention)
            elif message.channel.name == "code-questions":
                task = "You are a assistant coder. Please respond to the following: "
                response = getResponse(f"{task} \n {message.content}")
                response_with_mention = f"{message.author.mention} {response}"
                async with message.channel.typing():
                    await message.channel.send(response_with_mention)
            elif message.channel.name == "pre-alpha":
                task = "You are my personal AI and I will be asking you questions through Discord bot and openai api. Please respond to the following: "
                response = getResponse(f"{task} \n {message.content}")
                response = getResponse(f"{task} \n {message.content}")
                history.append(response)
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
        response = getResponse(message.content)
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

    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    bot = commands.Bot(command_prefix='?', description=description, intents=intents)

    vars = get_variables("./.env")
    bot.run(vars["REXTOPIA_TOKEN"])


# https://discord.com/api/oauth2/authorize?client_id=1115936819608039487&permissions=8&scope=applications.commands%20bot



