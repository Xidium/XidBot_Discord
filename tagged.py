import discord
import os
import random

meme_dir = './tagmemes/'
async def MemeResponse(message):

    await message.channel.send('Do you feel bad for how bad you are?')
    #Select Random Image
    meme_file = meme_dir + random.choice(os.listdir(meme_dir))
    await message.channel.send(file=discord.File(meme_file))

