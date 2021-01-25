#image api
#import stuff 
from bottle import run, request, response, route, redirect, template, get, post, static_file
import random

from PIL import Image
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
cards = Image.open('classic-playing-cards.jpg')


#globals
PORT = 9999
SERVER = f"http://localhost:{PORT}"
tabels = {}
players = {}

#crop card form cards sprite
def select_card(source,x, y):
    width  = int(source.width/13)
    height = int(source.height/4)
    y_start = y * height
    x_start = x * width
    np_cards = np.array(cards)
    #crop y,x 
    card = np_cards[y_start:y_start+height,x_start:x_start+width]
    return Image.fromarray(card)

#combine card images into one  
def show_hand(cards):
    width  = int(cards[0].width)
    height = int(cards[0].height)
    #blank images as background
    dst = Image.new('RGB',(width*len(cards),height))
    for i in range(len(cards)):
        dst.paste(cards[i],(width*i,0))
    return dst


@route('/')    
def home(): 
    return  ''' 
                <h2>commands</h2>
                <ul>
                <li>join /table id/ player id </li> 
                <li>switch/table id/ player id / player card index / table card index</li>
                <li>img/filename</li>
                <li>etc...</li>     
            '''

###server image ####
@route('/img/<filename>')
def server_static(filename):
    #headers: {'Content-Type': 'image/jpg'},
    response.content_type = 'image/jpg'
    return static_file(filename, root='.')


@route('/cards/<table_id>/<card1>/<card2>/<card3>')
def generate_img(table_id,card1,card2,card3):
    pair1 = card1.split(':')
    pair2 = card2.split(':')
    pair3 = card3.split(':')
    #arguments
    card1 = select_card(cards,int(pair1[0]),int(card1[2]))
    card2 = select_card(cards,int(pair2[0]),int(card2[2]))
    card3 = select_card(cards,int(pair3[0]),int(card3[2]))
    img = show_hand((card1,card2,card3))
    img.save(f"{table_id}-hand.jpg")
    url = f"{SERVER}/img/{table_id}-hand.jpg"
    return {"img":url, "success":True}

### server image ####


### game logic ###
tables = {}
from GameClasses.Player import Player
from GameClasses.Table import Table 


#routes

#create the table
@get("/setup/<table_id>")
def setup(table_id):
    if not table_id in tables:
        tables[table_id]= Table(table_id)
        
        return { "table":table_id, "player":"", "success":True}
    #already in tables
    return {"table":table_id, "player":"", "success":False} 

#player join the table 
@get("/join/<table_id>/<player_id>")
def join_table(table_id, player_id):
    if table_id in tables:
        table = tables[table_id]
        player = Player(player_id, True)
        #checks if player can join
        success = table.join(player)
        return   {"table":table_id, "success":success}
    else: 
       return {"table":table_id, "success":False}

@get("/begin/<table_id>")

def begin_game(table_id):
    if not table_id in tables: 
        return {"table":table_id, "success":False}
    if len(tables[table_id].players) < 3: 
        #add ai
        ai = Player('BOT', False)
        tables[table_id].join(ai)

    start_player = tables[table_id].begin()
    return {"table":table_id, "next":start_player, "success":True}
    
  
#moves
@get("/switch/<table_id>/<player_id>/<card_player>/<card_table>")
def move_switch(table_id, player_id, card_player, card_table):
    if table_id in tables: 
        result =  tables[table_id].switch(player_id,int(card_player),int(card_table))
        return {"next":tables[table_id].current_player, 'result':result,  "success":True}
    return { "next":player_id, "success":False}


@get("/pass/<table_id>/<player_id>")
def move_pass(table_id, player_id):
    if table_id in tables:  
        result = tables[table_id].player_pass(player_id)
        return {"next": tables[table_id].current_player, 'result':result, "success":True}
    return { "next":player_id, "success":False}


#info
@get('/table_info/<table_id>')
def print_tables(table_id):
    _info = ""
    for table_id in tables: 
        table = tables[table_id]
        print("table id",table.id)
        for player_id in table.players:
            _player = table.players[player_id]
            _info += f"player: {_player.id} has score {_player.calc_score()} , with hand {_player.hand} \n"
    return {'table':table_id, "info": _info}

         

if __name__ == "__main__":
    run(host='localhost',reloader=False, debug=True, port=PORT)




