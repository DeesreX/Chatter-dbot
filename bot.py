# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands
import random
import openai
import requests
from requests.structures import CaseInsensitiveDict
import json




# Set up your OpenAI API credentials
openai.api_key = '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'
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
    print('------')

@bot.event
async def on_message(message):
    allowed = ["DeesreX", "NO.", "Mage"]
    # Check if the message is sent by a user and not a bot
    async with message.channel.typing():
        if message.author.name in allowed:
            # check what channel
            if message.channel.name == "chat":
                async with message.channel.typing():
                    response = getResponse(message.content)
                    response_with_mention = f"{message.author.mention}, {response}"
                    await message.channel.send(response_with_mention)
            elif message.channel.name == "image-generation":
                image_url = getImageResponse(message.content)
                embed = discord.Embed()
                embed.set_image(url=image_url)
                response_with_mention = f"{message.author.mention}"
                async with message.channel.typing():
                    await message.channel.send(response_with_mention, embed=embed)
            elif message.channel.name == "code-explained":
                task = "Explain the code"
                response = getResponse(f"{task} \n {message.content}")
                response_with_mention = f"{message.author.mention} {response}"
                async with message.channel.typing():
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

    bot.run(REXTOPIA_TOKEN)


# https://discord.com/api/oauth2/authorize?client_id=1115936819608039487&permissions=8&scope=applications.commands%20bot