import random
#player
class Player: 
    def __init__(self,id,is_player):
        self.canmove = False; 
        self.id = id; 
        self.hand = []
        self.player = is_player
    def pick_cards(self,deck):
        #return [(8,0),(8,1),(8,2)]
        for i in range(3):
            random.shuffle(deck)
            card = deck.pop()
            self.hand.append(card)
            
            
    def calc_score(self):
        if self.hand == []: 
            return False
        if self.hand[0][0] == self.hand[1][0]: 
            if self.hand[0][0] == self.hand[2][0]: 
                return 30.5 
        
        score = [0,0,0,0]   
        for card in self.hand: 
            value, color = card[0],card[1]
            if value <= 9:
                score[color] += card[0]+1 #correct for index
            if value > 9 and value < 13: 
                score[color] += 10
            if value == 0: 
                score[color] += 11       
        return max(score)
                        
                        