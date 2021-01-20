import random
#game                
class Table:
    def __init__(self,table_id):
        self.id = table_id
        self.players = {} #max 3
        self.player_ids = [] #list of shuffeld player_id's that determin the playing order. 
        self.current_player = None #player that is allowed to make a move
        self.next_player = None #itterable
        self.deck = []
        self.cards = [] 
        self.began = False
        
    
    def create_deck(self): 
        for j in range(0,4): 
            for i in range(6, 13): 
                self.deck.append( (i,j) )

    #draws 3 cards
    def pick_cards(self): 
        for i in range(3): 
            random.shuffle(self.deck)
            card = self.deck.pop()
            self.cards.append(card)
    
    '''?? this needs some attention'''      
    def start(self, table_id, player_id): 
        if(not self.id):
            self.id = table_id; 
            return self.id
        if(player_id in self.players):
            self.restart()
            return self.id
        return "shut the up, you're not even at this table"
       
        
    #join internally 
    '''create a player, deal hand ,adds player to table.players'''
    def join(self,player):
        if self.began: 
            return "begone"
        if len(self.players) >= 3: 
            return "table is full"
        if not player in self.players:
            #save player
            self.players[player.id] = player
            return '1'
        return "0"
        
            
    
    def begin(self): 
        '''create a deck, set game state true, deal cards to players'''
        self.create_deck()
        self.began = True
        self.pick_cards()
        
        #playing order
        self.player_ids = list(self.players.keys())
        self.next_player = self.next_player_generator(self.player_ids)
        self.current_player = next(self.next_player)
        
        #assinging cards
        for player_id in self.players:
            player = self.players[player_id]
            player.canmove = True
            player.pick_cards(self.deck)
       
    # todo replace by the begin class
    def restart(self):
        print("restaring game")
        self.begin()
    
    def endgame(self):
        print("END, player scores:") 
        for _id in self.players: 
            player = self.players[_id]
            print(_id,player.calc_score())
        
    
    def delete(self, table_id): 
         if self.id == table_id and table_id in tables: 
            del tables[table_id]
    
    '''call at the beginning of a move to check if player is allowed to make a move'''
    def move(self, player_id):
        #check if its this players turn
        if player_id == self.current_player: 
            #if player pass at his last turn
            if not self.players[player_id].canmove: 
                return self.endgame()
            
            self.current_player = next(self.next_player)
            print("next player=>", self.current_player)
            return True
        else: 
            print(self.current_player)
            print(F"sorry this player is not allowd to make a move {player_id} != {self.current_player}")
            return False 
 
    def next_player_generator(self,players): 
        while True:
            for _id in players: 
                yield _id
    
    #moves: 
    def switch(self,player_id,A, B):
        if self.move(player_id):
            A= A-1;  
            B= B-1; 
            if A in range(0,3) and B in range(0,3):
                _player = self.players[player_id]
                #swap
                _player.hand[A], self.cards[B] = self.cards[B], _player.hand[A]
    
    def player_pass(self,player_id): 
           if self.move(player_id):
            self.players[player_id].canmove = False
