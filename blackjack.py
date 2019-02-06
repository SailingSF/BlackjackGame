'''
Blackjack game
'''

import random

suits = ('Hearts','Diamonds','Spades','Clubs')
ranks = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

#creation of card class, cards have a suit and rank. string function to display card value
class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return self.rank+ " of " +self.suit

#creation of a deck with one of every rank in every suit
#shuffle function to randomize order
class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n'+ card.__str__()
        return "The deck has: "+deck_comp    

    def shuffle(self):
        random.shuffle(self.deck)
    
    def deal(self):
        single_card = self.deck.pop() #one card is a .pop() off of the deck so it cannot be reselected
        return single_card

#class for a hand, each player including the dealer has a hand
class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # an attribute to keep track of aces
    
    def add_card(self,card):
        #card passed in from Deck.deal
        self.cards.append(card)
        self.value += values[card.rank]
        
        #track aces
        if card.rank == 'Ace':
            self.aces += 1
                
    
    def adjust_for_ace(self):
        #If total value goes over 21 and have an ace, change value of Ace to 1, removes one from ace
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

# chips class that each player will have and how to change chips depending on game outcome
class Chips:
    
    def __init__(self, total = 100):
        self.total = total
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    # blackjack happens when player reaches 21 exactly, payout is different
    def blackjack(self):
        self.total += 1.5*self.bet
    
    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    '''
    function to take bets
    try/except loop if input is not an integer
    check to make sure you have enough chips to bet
    '''
    while True:
        try:
            chips.bet = int(input("How many chips would you like to bet? "))
        except:
            print("Sorry, please enter an integer")
        else:
            if chips.bet > chips.total:
                print(f"You don't have enough chips. You have {chips.total}")
            else:
                break

# a hit adds a card to your hand, need to adjust for ace incase there it wasn an ace
def hit(deck,hand):
    
    hand.add_card(deck.deal())
    hand.adjust_for_ace()
                
def hit_or_stand(deck,hand):
    '''
    function to ask for player input of hit or stand
    '''
    global playing  # to control an upcoming while loop
    
    while True:
        x = input("Hit or Stand? Enter h or s")
        
        if x[0].lower() == 'h':
            hit(deck,hand)
            
        elif x[0].lower() == 's':
            print("Player turn over.")
            playing = False
        
        else:
            print("Please enter 'h' for Hit or 's' for Stand")
            continue
        break

def show_some(player,dealer):
    # show the face up cards, one of dealers and all of players
    print(f"Dealer's hand: \n{dealer.cards[1]} \n")
    print("Players hand: \n")
    for card in player.cards:
        print(card)
    print(f"You have {player_hand.value}")
    
    
def show_all(player,dealer):
    # after player turn show all cards including all dealer's
    print("Dealer's hand: \n")
    for card in dealer.cards:
        print(card)
    print(f"Dealer has {dealer_hand.value}")
    print("\nPlayers Hand:\n")
    for card in player.cards:
        print(card)

'''
Game outcome functions
Includes a print of what happened and runs the chips consequence function
'''
def player_busts(player, dealer, chips):
    print("Player busts! You lost your bet")
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print(f"Player WINS! You won ${chips.bet}")
    chips.win_bet()
    
def dealer_busts(player, dealer, chips):
    print(f"Dealer busts! You won ${chips.bet}")
    chips.win_bet()
          
def dealer_wins(player, dealer, chips):
    print("Dealer wins! You lost your bet")
    chips.lose_bet()
          
def player_blackjack(player, dealer, chips):
    print(f"BLACKJACK!! You win ${1.5*chips.bet}")
    chips.blackjack()
          
def push():
    print("PUSH. Bets are returned")

# end of outcome functions
chips_value = 100 # initial value of chips at first game run
while True:
    '''
    Game logic
    while loop runs until it is broken by player choosing to not run again
    game is set up and then proper functions are called to run the game
    '''
    # Print an opening statement
    print("Welcome to my blackjack game!")
    
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    
    #possibly add multiple players later
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    
    
    
        
    # Set up the Player's chips
    player_chips = Chips(chips_value)
    
    # Prompt the Player for their bet
    take_bet(player_chips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)

    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand)
        
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value == 21:
            player_blackjack(player_hand,dealer_hand,player_chips)
        elif player_hand. value > 21:
            player_busts(player_hand,dealer_hand,player_chips)

            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value < 21:
        
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)
    
        # Show all cards
        show_all(player_hand, dealer_hand)
        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push()
            
    
    # Inform Player of their chips total 
    print(f"\nPlayer total chips are {player_chips.total}")
    chips_value = player_chips.total # reassigning chips value if another game is played
    # Ask to play again
    new_game = input("Would you like to play another hand? y/n")
    
    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        winnings = player_chips.total - 100
        print(f"Game is over! your net change is ${winnings}")
        break

'''
End of game.
To do: add multiple players, imporve formatting
'''
