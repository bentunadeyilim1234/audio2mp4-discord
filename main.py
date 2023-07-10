import video_maker, discord, os
from dotenv import load_dotenv
import json

with open("settings.json", "r", encoding='utf-8', errors='ignore') as f:
    settings = json.load(f)

messageTrigger, requiredRoles, allowedExtensions = settings["messageTrigger"], settings["allowedRoles"], tuple(settings["allowedExtensions"])

load_dotenv()

token = os.getenv("DISCORD_TOKEN")
client = discord.Client(intents=discord.Intents.all())

async def reply(audio_file, message: discord.message.Message):
    path = video_maker.generate(audio_file)
    if message:
       await message.reply(file=discord.File(path))
    os.remove(path)
    os.remove(audio_file)

@client.event
async def on_message(message: discord.message.Message):
    role_exists = any(role.lower() in [role.name.lower() for role in message.author.roles] for role in requiredRoles)
    if str(message.attachments) == "[]":
        return
    if messageTrigger and (message.content != messageTrigger):
        return
    split_v1 = str(message.attachments).split("filename='")[1]
    filename = str(split_v1).split("' ")[0]
    if filename.endswith(allowedExtensions):
        if requiredRoles and not role_exists:
            return
        path = "files/{}".format(filename)
        await message.attachments[0].save(fp=path)
        await reply(path, message)

client.run(token)