# black jack in python wth pygame!
import copy
import random
import pygame
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
# from django.shortcuts import redirect
from button import Button
import fuzzylogic as fl

pygame.init()
# game variables
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

values= {
  "2": 2,
  "3": 3,
  "4": 4,
  "5": 5,
  "6": 6,
  "7": 7,
  "8": 8,
  "9": 9,
  "10": 10,
  "A": 11,
  "J": 10,
  "K": 10,
  "Q": 10,

}


one_deck = 4 * cards
decks = 4
WIDTH = 1400
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT],pygame.FULLSCREEN)
bg_img = pygame.image.load('bb.jpg')
bg_img = pygame.transform.scale(bg_img,(WIDTH,HEIGHT))
screen = pygame.display.set_mode([WIDTH, HEIGHT],pygame.FULLSCREEN)
bg_img2 = pygame.image.load('bdb.png')
bg_img2 = pygame.transform.scale(bg_img2,(WIDTH,HEIGHT))
bg_img1= pygame.image.load('bg.jpg')
bg_img1= pygame.transform.scale(bg_img1,(WIDTH,HEIGHT-100))

runing = True
i=0

pygame.display.set_caption('Pygame Blackjack!')
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 25)
smaller_font = pygame.font.Font('freesansbold.ttf', 20)
active = 2 
# win, loss, draw/push
records = [0, 0, 0, 0]
score_board = [0, 0, 0]
player_score = 0
dealer_score = 0
initial_deal = False
my_hand = []
AI_hand = []
AI_score = 0
dealer_hand = []
outcome = 0
game_deck = 0
reveal_dealer = False
hand_active = False
outcome = 0
add_score = False
s_board = [0,0,0]
results = ['', 'PLAYER BUSTED o_O', 'Player WINS! :)', 'DEALER WINS :(', 'TIE GAME...','AI_WINS! ^_^']


# deal cards by selecting randomly from deck, and make function for one card at a time
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card - 1])
    current_deck.pop(card - 1)
    return current_hand, current_deck


# draw scores for player and dealer on screen

def draw_scores(player, dealer,ai):
    screen.blit(font.render(f'Player_Point[{player}]', True, 'white'), (550, 400))
    screen.blit(font.render(f'AI_Point[{ai}]', True, 'white'), (1050, 400))
    if reveal_dealer:
        screen.blit(font.render(f'Dealer_Point[{dealer}]', True, 'white'), (250, 400))
       


# draw cards visually onto screen
def draw_cards(player, dealer, reveal,AI):
    
    for i in range(len(player)):
        pygame.draw.rect(screen, 'white', [500 + (70 * i), 160 + (5 * i), 120, 220], 0, 5)
        screen.blit(font.render(player[i], True, 'black'), (505 + 70 * i, 165 + 5 * i))
        screen.blit(font.render(player[i], True, 'black'), (505 + 70 * i, 335 + 5 * i))
        pygame.draw.rect(screen, 'red', [500 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)
        
    for i in range(len(AI)):
        pygame.draw.rect(screen, 'white', [1000 + (70 * i), 160 + (5 * i), 120, 220], 0, 5)
        screen.blit(font.render(AI[i], True, 'black'), (1005 + 70 * i, 165 + 5 * i))
        screen.blit(font.render(AI[i], True, 'black'), (1005+ 70 * i, 335 + 5 * i))
        pygame.draw.rect(screen, 'yellow', [1000 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)
        

    # if player hasn't finished turn, dealer will hide one card
    for i in range(len(dealer)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 160 + (5 * i), 120, 220], 0, 5)
        if i != 0 or reveal:
            screen.blit(font.render(dealer[i], True, 'black'), (75 + 70 * i, 165 + 5 * i))
            screen.blit(font.render(dealer[i], True, 'black'), (75 + 70 * i, 335 + 5 * i))
        else:
            screen.blit(font.render('???', True, 'black'), (75 + 70 * i, 165 + 5 * i))
            screen.blit(font.render('???', True, 'black'), (75 + 70 * i, 335 + 5 * i))
        pygame.draw.rect(screen, 'blue', [70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)


# pass in player or dealer hand and get best score possible
def calculate_score(hand):
    # calculate hand score fresh every time, check how many aces we have
    hand_score = 0
    aces_count = hand.count('A')
    for i in range(len(hand)):
        # for 2,3,4,5,6,7,8,9 - just add the number to total
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])
        # for 10 and face cards, add 10
        if hand[i] in ['10', 'J', 'Q', 'K']:
            hand_score += 10
        # for aces start by adding 11, we'll check if we need to reduce afterwards
        elif hand[i] == 'A':
            hand_score += 11
    # determine how many aces need to be 1 instead of 11 to get under 21 if possible
    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score -= 10
    return hand_score


def AI_cards(hand,current_deck):
    
    value = calculate_score(hand)
    need = 21 - value
    more=0
    less=0
    card_A=0
    total_card = len(current_deck)
    for i in range(len(current_deck)):
        if (current_deck[i] == "A"):
            card_A = card_A+1
        if (values[current_deck[i]] < need):
            less += 1
        else:
            more +=1
    prob_higher=float(more/total_card * 1.0)
    prob_lower=float(less/total_card * 1.0)
    risk=float(card_A/total_card * 1.0)
    if(prob_lower+ (2*risk)>=prob_higher or prob_higher-prob_lower<.001):
        hand, current_deck = deal_cards(hand, current_deck)
      
    return hand,current_deck
            
    
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("font.ttf", size)

# draw game conditions and buttons
def draw_game(act, record=[0,0,0,0], result=[0,0,0],s_board=[0,0,0]):
    button_list = []
    # initially on startup (not active) only option is to deal new hand
    if act == 0:
        screen.blit(bg_img,(0,0))

        #screen.fill('Black')
        deal1 = pygame.draw.rect(screen, 'white', [900, 50, 300, 80], 0, 2)
        pygame.draw.rect(screen, 'purple', [900, 50, 300, 80], 3, 5)
        deal_text = font.render('Black Jack', True, 'black')
        screen.blit(deal_text, (970, 80))
        button_list.append(deal1)
        deal2 = pygame.draw.rect(screen, 'white', [900, 250, 300, 80], 0, 2)
        pygame.draw.rect(screen, 'purple', [900, 250, 300, 80], 3, 5)
        deal_text = font.render('Black Jack 2.0', True, 'black')
        screen.blit(deal_text, (970, 280))
        button_list.append(deal2)
        deal3 = pygame.draw.rect(screen, 'white', [900, 450, 300, 80], 0, 2)
        pygame.draw.rect(screen, 'purple', [900, 450, 300, 80], 3, 5)
        deal_text = font.render('Wanna Back?', True, 'black')
        screen.blit(deal_text, (970, 480))
        button_list.append(deal3)
        
        
    
    elif act == 2:
            
            #screen.fill('3F1651')
            screen.blit(bg_img2,(0,0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = get_font(100).render("BLACK JACK", True, "Yellow")
            MENU_RECT = MENU_TEXT.get_rect(center=(700, 200))


            color = "#03fce3"

            PLAY_BUTTON = Button(image=pygame.image.load("Play Rect.png"), pos=(700, 350), 
                                text_input="PLAY", font=get_font(55), base_color=color, hovering_color="White")
           
            
            QUIT_BUTTON = Button(image=pygame.image.load("Quit Rect.png"), pos=(700, 550), 
                                text_input="QUIT", font=get_font(55), base_color=color, hovering_color="White")

            screen.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(screen)
            return PLAY_BUTTON,QUIT_BUTTON,MENU_MOUSE_POS
    elif act == 1:
        #screen.fill('#660099')
        hit = pygame.draw.rect(screen, 'white', [0, 550, 300, 50], 0, 5)
        pygame.draw.rect(screen, 'purple', [0, 550, 300, 50], 3, 5)
        hit_text = font.render('HIT ME', True, 'black')
        screen.blit(hit_text, (105, 565))
        button_list.append(hit)
        
        stand = pygame.draw.rect(screen, 'white', [300, 550, 300, 50], 0, 5)
        pygame.draw.rect(screen, 'purple', [300, 550, 300,50], 3, 5)
        stand_text = font.render('STAND', True, 'black')
        screen.blit(stand_text, (405, 565))
        button_list.append(stand)
        
        quite = pygame.draw.rect(screen, 'white', [600, 550, 300, 50], 0, 5)
        pygame.draw.rect(screen, 'purple', [600, 550, 300,50], 3, 5)
        stand_text = font.render('QUIT', True, 'black')
        screen.blit(stand_text, (705, 565))
        button_list.append(quite)
        
        score_text = smaller_font.render(f'Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}  AI : {record[3]}', True, 'white')
        screen.blit(score_text, (5, 640))
        
        score_text = smaller_font.render(f'Players score: {s_board[0]}   Dealers score: {s_board[1]}   AI score: {s_board[2]}', True, 'white')
        screen.blit(score_text, (5, 660))
        
        
    # if there is an outcome for the hand that was played, display a restart button and tell user what happened
    if result != 0 and active == 1:
        screen.blit(font.render(results[result], True, 'white'), (15, 25))
        deal = pygame.draw.rect(screen, 'white', [150, 220, 300, 120], 0, 5)
        pygame.draw.rect(screen, 'green', [150, 220, 300, 120], 3, 5)
        pygame.draw.rect(screen, 'black', [153, 223, 294, 117], 3, 5)
        deal_text = font.render('NEW HAND', True, 'black')
        screen.blit( deal_text, (165, 250))
        button_list.append(deal)
    return button_list

#results = ['', 'PLAYER BUSTED o_O', 'Player WINS! :)', 'DEALER WINS :(', 'TIE GAME...','AI_WINS! ^_^']


# check endgame conditions function
def check_endgame(AI_S,hand_act, deal_score, play_score, result, totals, add,sc_board):
    # check end game scenarios is player has stood, busted or blackjacked
    # result 1- player bust, 2-win, 3-loss, 4-push
    
    if not hand_act and deal_score >= 17:
        if play_score > 21:
            result =  1
            
            
        elif (deal_score < play_score <= 21 and  AI_S < play_score <=21  )or (deal_score > 21 and play_score > AI_S and play_score <=21) or (dealer_score > 21 and play_score<=21 and AI_S>21):
            result = 2
          
            
        elif (play_score < deal_score <= 21 and AI_S < deal_score <= 21) or (AI_S>21 and play_score<deal_score<=21) :
            result = 3
          
            
        if (((AI_S<=21 and play_score>21 and deal_score>21) or (deal_score<=21 and deal_score<=AI_S) or (play_score<AI_S<=21)) and AI_S<=21) :
             result = 5
         
             
        elif (AI_S == dealer_score or AI_S == player_score):
             result = 4
            
        if add:
            #0-player 1-Dealer 2-Tie 3-AI
            if result == 1 or result == 3 :
                totals[1] += 1
                sc_board[0] = sc_board[0] 
                sc_board[1] = sc_board[1] + 20
                sc_board[2] = sc_board[2] + 20
                
            elif result == 2:
                totals[0] += 1
                sc_board[0] = sc_board[0] + 30
                sc_board[1] = sc_board[1] 
                sc_board[2] = sc_board[2] 
                
            elif result == 5 :
                totals[3] +=1
                sc_board[0] = sc_board[0] 
                sc_board[1] = sc_board[1] 
                sc_board[2] = sc_board[2] + 30
                
            else: 
                totals[2] += 1
                
            add = False
            
    return result, totals, add, score_board



#BlackJack2.0 starting

class Mem():
   
    logo_frame = None
    new_card = ''
    first_card = ''
    click_count = 0
    found_matches = 0
    total_tries = 0
    match_list = []
    blank_cards = []
    card_images = []
    all_clicks = 0
    target_clicks = 30
    stat_bar = None
    card = None
    num_pairs = 8  
    level = 1  



def updt_status_bar(txt):
    Mem.stat_bar.config(text=txt)
    Mem.stat_bar.update()


def logo():
  
    Mem.logo_frame = tk.Frame(root)
    Mem.logo_frame.grid(row=0, columnspan=10)
    logo_image = Image.open('bb.jpg')
    # Increase the size of the image
    new_size = (1500, 300)  # Set the desired size
    logo_image = logo_image.resize(new_size, Image.ANTIALIAS)
  
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(Mem.logo_frame, image=logo_photo)
    logo_label.logo_image = logo_photo
    logo_label.grid(padx=0, pady=0, row=0, column=0)


def complete_game_as_winner():
    messagebox.showinfo('Winner',
                        'Well done you have completed the game!\n\n'
                        'Now do it again in even less clicks!')
    root.destroy()




def level_up():
    # Define fuzzy sets for input and output variables
    clicks = fl.FuzzySet(0, 100, 200)  # Represents the number of clicks
    difficulty = fl.FuzzySet(0, 1)  # Represents the difficulty level

   # Define fuzzy rules
    rules = [
       fl.FuzzyRule([clicks['low']], difficulty['high']),
       fl.FuzzyRule([clicks['medium']], difficulty['medium']),
       fl.FuzzyRule([clicks['high']], difficulty['low'])]
   

   # Fuzzify the input (number of clicks)
    input_clicks = Mem.all_clicks
    clicks_membership = clicks.fuzzify(input_clicks)

   # Perform fuzzy inference to determine difficulty
    engine = fl.FuzzyEngine(rules)
    difficulty_membership = engine.execute({'clicks': clicks_membership}, {'difficulty': difficulty})
    # Defuzzify the output (difficulty)
    output_difficulty = difficulty.defuzzify(difficulty_membership)
    if Mem.level == 1 and Mem.all_clicks < 31:
        messagebox.showinfo('Congratulations:',
                            'Well done, level 1 completed\n\n'
                            'Click OK to play level 2.')
        Mem.level = 2
        Mem.num_pairs = 12
        Mem.target_clicks = 60
        return

    if Mem.level == 2 and Mem.all_clicks < 61:
        messagebox.showinfo('Congratulations:',
                            'Well done, level 2 completed\n\n'
                            'Click OK to play level 3.')
        Mem.level = 3
        Mem.num_pairs = 16
        Mem.target_clicks = 90
        return

    if Mem.level == 3 and Mem.all_clicks < 91:
        complete_game_as_winner()
        return

    # Repeat level.
    if output_difficulty > 0.6:
        messagebox.showinfo('Congratulations:')
        
    else:
        messagebox.showinfo('Good try:')


def we_have_a_winner():
    updt_status_bar('Completed puzzle in: '
                    + str(Mem.all_clicks) + ' clicks')

    Mem.new_card = ''
    Mem.first_card = ''
    Mem.click_count = 0
    Mem.found_matches = 0
    Mem.total_tries = 0
    Mem.match_list = []
    Mem.blank_cards = []
    Mem.card_images = []
    Mem.stat_bar = None
    Mem.card = None

    level_up()  # Do we up a level or not?

    # Start game.
    Mem.all_clicks = 0
    create_status_bar()
    create_game_board()


def level_msg():
    if Mem.level == 1:
        updt_status_bar('Complete this level within 30 clicks'
                        ' to advance to level 2.')
        root.title('Black_Jack2.0     Level 1')
    if Mem.level == 2:
        updt_status_bar('Complete this level within 60 clicks'
                        ' to advance to level 3.')
        root.title('Black_Jack2.0    Level 2')

    if Mem.level == 3:
        updt_status_bar('Complete this level within 90 clicks'
                        ' to complete game.')
        root.title('Black_Jack2.0     Level 3')


def get_png_list(loc):
    """Get all images in 'png' dir."""
    pngs = [f for f in os.listdir(loc) if f[-4:] == '.png']
    return [os.path.join(loc, f) for f in pngs]


def check_match():
    Mem.total_tries += 1
    Mem.new_card.img = Mem.card
    Mem.new_card.config(image=Mem.new_card.img)
    Mem.first_card.img = Mem.card
    Mem.first_card.config(image=Mem.first_card.img)

    for item in Mem.blank_cards:
        if item.cget('text') not in Mem.match_list:
            item.bind('<Button-1>', on_click)

    Mem.click_count = 0


def on_click(event):
    Mem.click_count += 1
    Mem.all_clicks += 1

    Mem.new_card = event.widget
    img = tk.PhotoImage(file=Mem.new_card.cget('text'))
    Mem.new_card.img = img
    Mem.new_card.config(image=img)

    if Mem.click_count == 1:
        Mem.first_card = Mem.new_card  # Put in holding space if 1st click.
        Mem.first_card.unbind('<Button-1>')
        updt_status_bar('Clicks:' + str(Mem.all_clicks) +
                        '-' + str(Mem.target_clicks))

    else:
        for item in Mem.blank_cards:
            item.unbind('<Button-1>')
        # FOUND MATCH: Unbind click events. Update match tracker.
        if Mem.new_card.cget('text') == Mem.first_card.cget('text'):
            Mem.match_list.append(Mem.new_card.cget('text'))
            Mem.found_matches += 1
            # print(Mem.found_matches)
            Mem.total_tries += 1
            Mem.click_count = 0
            for item in Mem.blank_cards:
                if item.cget('text') not in Mem.match_list:
                    updt_status_bar('Clicks:' + str(Mem.all_clicks) +
                                    '-' + str(Mem.target_clicks))
                    item.bind('<Button-1>', on_click)
            if Mem.found_matches == Mem.num_pairs:
                we_have_a_winner()
                updt_status_bar('Clicks:' + str(Mem.all_clicks) +
                                '-' + str(Mem.target_clicks))

                # print('Total Tries = ' + str(Mem.total_tries))

        else:
            for item in Mem.blank_cards:
                item.unbind('<Button-1>')
                updt_status_bar('Clicks:' + str(Mem.all_clicks) +
                                '-' + str(Mem.target_clicks))

            Mem.new_card.after(1000, check_match)


def on_button_click():
    #root.destroy()
    global active
    active = 2
    root.destroy()
    #pygame.quit()
     
def create_game_board():
    
    button = tk.Button(root, text="CLOSE GAME", command=on_button_click,font=("Arial", 10), fg="white")
    button.config(width=20, height=5)
    button.configure(bg="purple")
    button.grid(row=0, column=0, padx=10, pady=10,sticky=tk.SE)

    image_dir = os.path.join(os.path.dirname(__file__), 'png')
    image_array = get_png_list(image_dir)

 # Create array with how many cards needed and double it.
    image_pairs = image_array[0:Mem.num_pairs]
    image_pairs = image_pairs * 2

 # Because we doubled, we need to re-shuffle order.
    random.shuffle(image_pairs)

    card_dir = os.path.join(os.path.dirname(__file__), 'card.png')
    Mem.card = tk.PhotoImage(file=card_dir)

 # Display card back images in a grid 8 wide.
    ro = 0
    col = 0

    game_board_frame = tk.Frame(root)
    game_board_frame.grid(row=1, column=0)
    game_board_frame.configure(background='#502963')

    for i in range(len(image_pairs)):
        Mem.blank_cards.append(tk.Label(game_board_frame))
        Mem.card_images.append(tk.PhotoImage(file=image_pairs[i]))
        Mem.blank_cards[i].img = Mem.card
        Mem.blank_cards[i].config(image=Mem.blank_cards[i].img)
        Mem.blank_cards[i].config(text=image_pairs[i])
        
        # Adjust the padding values to increase the size of each card
        Mem.blank_cards[i].grid(row=ro, column=col, padx=10, pady=10)
        
        Mem.blank_cards[i].bind('<Button-1>', on_click)
        
        col += 1
        if col == 8:
            col = 0
            ro += 1
            
    # Adjust the weights and minimum sizes of the rows and columns
    for row in range(ro):
        game_board_frame.grid_rowconfigure(row, weight=1, minsize=210)  # Increase the minimum size of each row
        
    for col in range(8):
        game_board_frame.grid_columnconfigure(col, weight=1, minsize=170)  # Increase the minimum size of each column


def create_status_bar():
    stat_frame = tk.Frame(root)
    stat_frame.grid(padx=0, pady=8,
                    row=4, columnspan=8,
                    sticky=tk.W + tk.E)

    Mem.stat_bar = tk.Label(stat_frame,
                            bg='#CBC3E3',
                            fg='black',
                            font=('ariel, 16'),
                            text='',
                            bd=1,
                            relief=tk.SUNKEN,
                            anchor=tk.W)
    Mem.stat_bar.pack(side=tk.BOTTOM, fill=tk.X)




def exit_app():
    ask_yn = messagebox.askyesno('Question', 'Confirm Quit?')
    if not ask_yn:
        return
    root.destroy()
    
# main game loop
run = True
while run:
    
   
    # run game at our framerate and fill screen with bg color
    timer.tick(fps)
    screen.fill('#301934')
    # initial deal to player and dealer
    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
            AI_hand, game_deck = deal_cards(AI_hand, game_deck)
            
        initial_deal = False
    # once game is activated, and dealt, calculate scores and display cards
    if active == 1:
        player_score = calculate_score(my_hand)
        AI_score = calculate_score(AI_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer,AI_hand)
        
        
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            #AI_score = calculate_score(AI_hand)
            #print(AI_score)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_scores(player_score, dealer_score,AI_score)
    if(active != 2):    
        buttons = draw_game(active, records, outcome, score_board)
    else:
        PLAY_BUTTON,QUIT_BUTTON,MENU_MOUSE_POS = draw_game(active, records, outcome, score_board)

    # event handling, if quit pressed, then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
        if event.type == pygame.MOUSEBUTTONUP:
            if active == 2:
               
                for button in [PLAY_BUTTON, QUIT_BUTTON]:
                     button.changeColor(MENU_MOUSE_POS)
                     button.update(screen)
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                     active = 0
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                     pygame.quit()
                pygame.display.update()
            elif active == 0:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    AI_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    reveal_dealer = False
                    outcome = 0
                    add_score = True
                elif buttons[2].collidepoint(event.pos):
                    active = 2
                elif buttons[1].collidepoint(event.pos):
                    root = tk.Tk()
                    root.title('Black Jack 2.0    Level 1')
                    root.attributes("-fullscreen", True)
                    root.resizable(False, False)
                    root.geometry('+550+300')
                    logo()
                    create_status_bar()
                    create_game_board()
                    root.protocol('WM_DELETE_WINDOW', exit_app)
                    root.mainloop()
                    pygame.display.update()
                    #pygame.quit()
            

                

            else:
                # if player can hit, allow them to draw a card
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    
                    print("hit")
                    my_hand, game_deck = deal_cards(my_hand, game_deck)  
                    AI_hand, game_deck = AI_cards(AI_hand, game_deck)
                    print(AI_hand)
                    
                # allow player to end turn (stand)
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                    
                elif buttons[2].collidepoint(event.pos):
                    screen.fill('Black')
                    active = 2
                   
                elif len(buttons) == 4:
                    if buttons[3].collidepoint(event.pos):
                        active = 1
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        AI_hand =[]
                        dealer_hand = []
                        outcome = 0
                        score_board = [0,0,0]
                        hand_active = True
                        reveal_dealer = False
                        outcome = 0
                        add_score = True
                        dealer_score = 0
                        player_score = 0


    # if player busts, automatically end turn - treat like a stand
    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True

    outcome, records, add_score, score_board = check_endgame(AI_score,hand_active, dealer_score,player_score, outcome, records, add_score,score_board)

    pygame.display.flip()
pygame.quit()





