import os
import re
import discord
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

projects = {}

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
    global projects
    if message.author.bot:
        return
    
    if "!pm" in message.content:
        response = "Unrecognized command, please use `!pm help` for a full command list"

        if "clear" in message.content:
            response = """```Projects has been cleared!```"""
            projects = {}

        if "vote" in message.content:
            token = message.content.lower().split()
            if token[-1] == "vote":
                response = """```Please specify the project that you want to vote: !pm vote [projectName]```"""
            else:
                projectName = token[-1]                
                if (projectName in projects):
                    for member in message.channel.members:
                        if not member.bot:
                            await member.send("""```Voting for {}```""".format(projectName))
                # try:
                #     if message.author in projects[token[-2]]['voters']:
                #         response = """@{}, you cannot vote multiple times!  """.format(message.author.split("#")[0])
                #     else:
                #         ratio = token[-1].split("/")
                #         ratio = int(ratio[0]) / int(ratio[1])
                #         projects[token[-2]]['vote'] += ratio
                #         projects[token[-2]]['voters'].add(message.author) 
                #         response = """@{}, thanks for voting!""".format(message.author.split("#")[0])
                # except:
                #     pass

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
                projectName = message.content.replace("!pm project add", "").strip().replace(" ","_").lower()
                if projectName:
                    if (projectName not in projects):
                        response = "{} has been added".format(projectName)
                        projects[projectName] = {'vote':0,'voters':set()}
                    else:
                        response = "{} is already exist!".format(projectName)

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
                    response = "```📋 List of saved projects:\n"
                    for index,project in enumerate(projects):
                        response = str(response) + str(1+index) + ". " + str(project) + " (" + str(projects[project]['vote']) + " votes) " + "\n"
                    response = response + "```"              

        await message.channel.send(response)

client.run(TOKEN)