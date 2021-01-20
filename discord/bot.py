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

    if command == 'ping':
        data = json_request(server_url+'https://jsonplaceholder.typicode.com/todos/1')
        if data: 
            await message.channel.send('Pong')
            return 


    if command == 'json':
        data = json_request(server_url+'https://jsonplaceholder.typicode.com/todos/1')
        if data: 
            await message.channel.send(str(data))
            return 

    #setup command
    if command == 'setup':
        data = json_request(server_url+'/setup/desperadoes')
        if data: 
            await message.channel.send(str(data))
            return 
    #join command
    if command == 'join':
        data = json_request(server_url+'/join/desperadoes/rutte')
        if data: 
            await message.channel.send(str(data))
            return 
    #switch command
    if command == 'switch':
        data = json_request(server_url+'/switch/desperadoes/rutte/2/2')
        if data: 
            await message.channel.send(str(data))
            return 
    #pass command
    if command == 'pass':
        data = json_request(server_url+'/pass/desperadoes/merkel')
        if data: 
            await message.channel.send(str(data))
            return 
client.run(read_token())

