import os
import re
import discord
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

projects = []

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "!pm" in message.content:
        response = "Unrecognized command, please use `!pm help` for a full command list"

        if "help" in message.content:
            response = """```Here are available commands:
        - Help Menu         : !pm help
        - Project Management: !pm project```"""

        if "project" in  message.content:
            response = """```Here are available commands for !pm project:
        - Add Project    : !pm project add [projectName]
        - Remove Project : !pm project remove [projectName]
        - Project list   : !pm project list```"""

            if "add" in message.content:
                response = "Please specify a name for the project"
                projectName = message.content.replace("!pm project add", "").strip()
                if projectName:
                    response = "{} has been added".format(projectName)
                    projects.append(projectName)

            if "remove" in message.content:
                response = "Please specify a name for the project"
                projectName = message.content.replace("!pm project remove", "").strip()                
                if projectName:
                    try:
                        index = projects.index(projectName)
                        response = "{} has been deleted".format(projectName)
                        projects.pop(index)
                    except:
                        response = "Can't find {}".format(projectName)

            if "list" in message.content:
                response = "There are no saved projects for now :("
                if projects:
                    response = "```List of saved projects:\n"
                    for project in projects:
                        response = response + project + "\n"
                    response = response + "```"              

        await message.channel.send(response)

client.run(TOKEN)