import discord
import requests
import nice
from discord.ext import commands
import yaml
import time


###Load token
try:
    with open('.\\credentials\creds.yaml') as file:
        creds = yaml.safe_load(file)
except Exception as e:
    print(e)
    exit()


token = creds['credentials']['token']

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if  '!random fact' in message.content.lower() or '!randomfact' in message.content.lower()  or '!randfact' in message.content.lower() or '!rf' in message.content.lower():   
        #start timer
        start_time = time.time()
        response = requests.get('https://en.wikipedia.org/api/rest_v1/page/random/summary').json()
        response_time = time.time()
        summary = response['extract']
        summary_time = time.time() 
       
        # print(start_time)
        # print(response_time)
        # print(summary_time)
        #print(f'Sending message about {title}')
        await message.channel.send(summary)        
        if 'stats' in message.content.lower():
            await message.channel.send(f'It took a total of {int((summary_time-start_time)*1000)}ms to process this entire message. \n{int((response_time - start_time) * 1000)}ms for the API call \n{int((summary_time - response_time)*1000)}ms to extract')

    if 'you just advanced to level' in message.content.lower() and message.author.name == 'MEE6':
        #print('New level up!')
        await message.channel.send(file=discord.File('celebrate-happy.gif'))


    
    if  message.content.lower() == 'nice'.strip('!').strip('.'):
        await nice.Nice(message, client)

    if '!channelnicescore' in message.content.lower():
        await nice.GetChannelNiceHighScores(message)
    
    if '!mynicescore' in message.content.lower():
        await nice.GetUserNiceScore(message)
    
    if '!globalnicescore' in message.content.lower():
        await nice.GetTopNiceHighcores(message)
    
    if '!servernicescore' in message.content.lower():
        await nice.GetServerNiceHighScores(message)


client.run(token)



