import sqlite3
import discord

sqlite3
async def Nice(message, client):
   await message.channel.send(file=discord.File('nice-south-park.gif'))
   await LogNice(message)
   
    
def GetSqlObj():
    try:
        con = sqlite3.connect('nice.db')
        cur = con.cursor()
    except Exception as e:
        print(e)
        return
    return con,cur

async def LogNice(message):    
    
    con,cur = GetSqlObj()

    user_id = message.author.id
    user_name = message.author.name.replace('\'','')
    channel_id = message.channel.id
    channel_name = message.channel.name.replace('\'','')
    guild_id = message.guild.id
    guild_name = message.guild.name.replace('\'','')


    ##############################
    #Check if user exists already#
    ##############################
    user_score_query = f'''
    Select
    NiceScore 
    FROM Nice

    Where
    UserID = '{user_id}' and
    ChannelID = '{channel_id}' and
    GuildID = '{guild_id}'
    '''

    current_score = cur.execute(user_score_query).fetchone()
    if current_score is None:
        create_user_statment = f'''
        Insert Into Nice
        (UserID, UserName, ChannelID, ChannelName,GuildID,GuildName,NiceScore)
        Values
        ('{user_id}','{user_name}','{channel_id}','{channel_name}','{guild_id}','{guild_name}',1)        
        ''' 

        try:
            cur.execute(create_user_statment)
            con.commit()
            print(f'Created user {user_name}:{user_id}')
        except Exception as e:
            print(e)
    else:

    #################
    #Update Existing#
    #################
    
        new_score = current_score[0]+1
        
        update_score_statment = f'''
        Update Nice
        Set  NiceScore = {new_score}

        Where
        UserID = '{user_id}' and
        ChannelID = '{channel_id}' and
        GuildID = '{guild_id}'
        '''
        cur.execute(update_score_statment)
        con.commit()


async def GetChannelNiceHighScores(message):
    con, cur = GetSqlObj()

    sql_query = f'''
    Select
    NiceScore,
    UserName    
    From Nice

    where ChannelID = '{message.channel.id}'

    Order by NiceScore Desc

    Limit 10        
    '''
    
    scores = cur.execute(sql_query).fetchall()
    

    response_string = f'```Nice Leaderboard for channel {message.channel.name}\n'
    formatted_table = FormatTable(('Score','UserName'),scores)
    response_string = response_string + formatted_table + '```'

    await message.channel.send(response_string)
    
async def GetUserNiceScore(message):

    con,cur = GetSqlObj()

    sql_query_channel = f'''
    Select
    'CurrentChannel' as responsetype,
    NiceScore
    from Nice

    Where
    UserID = '{message.author.id}' and
    ChannelID = '{message.channel.id}'
    '''
    
    sql_query_server = f'''
    Select
    'CurrentServer' as responsetype,
    Sum(NiceScore)
    from Nice

    Where
    UserId = '{message.author.id}'and
    GuildID = '{message.guild.id}'
    '''

    sql_query_total = f'''
    Select
    'Total' as responsetype,
    Sum(NiceScore)
    From Nice

    Where
    UserId = '{message.author.id}'
    '''

    cur_channel_score = cur.execute(sql_query_channel).fetchone()    
    cur_server_score = cur.execute(sql_query_server).fetchone()
    cur_total_score = cur.execute(sql_query_total).fetchone()

    scores= ((cur_channel_score),(cur_server_score),(cur_total_score))


    response_string = f'```{message.author.name} Nice Stats\n'+ FormatTable(('Type','Score'),scores) + '```'
    #formatted_table = FormatTable(('Type','Score'),scores)
    await message.channel.send(response_string)

async def GetTopNiceHighcores(message):
    con, cur = GetSqlObj()

    sql_query = f'''
    Select
    UserName,
    Sum(NiceScore)
    From Nice

    Group By UserName
    Order By NiceScore Desc
    Limit 10
    '''
       
    scores = cur.execute(sql_query).fetchall()
    response_string = f'```Global Nice Leaderboard\n'+ FormatTable(('Type','Score'),scores) + '```'
    await message.channel.send(response_string)

async def GetServerNiceHighScores(message):
    con,cur = GetSqlObj()

    sql_query = f'''
    Select
    UserName,
    Sum(NiceScore)
    From Nice

    Where
    GuildID = '{message.guild.id}'
    
    Group By UserName
    Order By NiceScore Desc
    Limit 10
    '''

    scores = cur.execute(sql_query).fetchall()
    response_string = f'```{message.guild.name} Nice Leaderboard\n'+ FormatTable(('Type','Score'),scores) + '```'
    await message.channel.send(response_string)


def FormatTable(headers, scores):

    col_width = 20

    #build the header string    
    header_string = ''
    for header in headers:
        #Conctact the new header onto the string
        header_string = header_string + header
        #Add required whitespace
        i=0
        while i < col_width - len(header):
            header_string = header_string + ' '
            i += 1
    #Add new line
    header_string = header_string + '\n'


    #build score string
    score_string = ''

    for score in scores:
        x = 0
        while x < len(headers):
            score_string = score_string + str(score[x])
            #add whitespace
            i=0
            while i < col_width - len(str(score[x])):
                score_string = score_string + ' '
                i += 1
            x += 1
        score_string = score_string + '\n'
    message_string = header_string+score_string
    return message_string



