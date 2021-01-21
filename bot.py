import discord
import requests
client = discord.Client()

prefix = '$'
server_url = "http://localhost:9999"

#FUNCTIONS
def read_token():
    f=open("token.txt", "r")
    if f.mode == 'r':
        token = f.read()
        if token and len(token) > 10:
            f.close()
            return token
    exit("no token")


'''handels commands from user input'''
def commands(msg):
    if msg:
        if msg[0] == prefix:
            return msg[1:]
    return False


''' make request with error handling''' 
def json_request(url):    
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        else:
            print(r.status_code)
    except:
        print(f"request to url {url} failt")
    
    return False


#EVENTS
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #grap command
    command = commands(message.content)
    channel_name = message.guild.name
    sender_name = message.author.name

   #test commands
    if command == 'ping':
            await message.channel.send('Pong')
            return 

    if command == 'msg-info':
            info = f"{message.author.name} from {message.guild.name}"
            await message.channel.send(info)
            return 

    if command == 'json':
        data = json_request('https://jsonplaceholder.typicode.com/todos/1')
        if data: 
            await message.channel.send(str(data))
            return 
   # end test commands


    #setup command: create a table with the table_id of text channel name
    if command == 'setup':
        data = json_request(server_url+f'/setup/{channel_name}')
        if data: 
            await message.channel.send(str(data))
            return 
    #join command: join table
    if command == 'join':
        data = json_request(server_url+f'/join/{channel_name}/{sender_name}')
        if data: 
            await message.channel.send(str(data))
            return 

    #begin command: create deck, deal cards, pick cards
    if command == 'begin':
        data = json_request(server_url+f'/join/{channel_name}/{sender_name}')
        if data: 
            await message.channel.send(str(data))
            return         
    
    #switch command, swap one card from your hand with a card on the table
    if command == 'switch':
        data = json_request(server_url+f'/switch/{channel_name}/{sender_name}/2/2')
        if data: 
            await message.channel.send(str(data))
            return 
    #pass command: pass, initialzing the end of the round (very other player can make last move)
    if command == 'pass':
        data = json_request(server_url+f'/pass/{channel_name}/{sender_name}')
        if data: 
            await message.channel.send(str(data))
            return 
client.run(read_token())

