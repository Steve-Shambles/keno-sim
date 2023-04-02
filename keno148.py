"""
    Keno Simulator V1 By Steve Shambles 2023

    Requirements:
    Pip3 install sounddevice
    pip3 install soundfile
    pip3 install Pillow

"""
import os
import random
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, Menu
import webbrowser as web

from PIL import Image, ImageTk
import sounddevice as sd
import soundfile as sf


root = tk.Tk()
root.title('Keno Simulator V1 By Steve Shambles 2023')
cfont = ('Courier', 11, 'bold')


class Fs():
    """ I know this is wrong, but this is how I work, sorry PEP8.
        All these variables are now effectively global.
        example: Fs.call_count"""
    amount_of_user_selections = 0
    ball_numb_frame = None
    ball_numb_lab = None
    called_number = 0
    call_count = 0
    call_counter_frame = None
    call_counter_lab = None
    clicked_buttons = []
    combo_stakes = ['£1', '£2', '£5', '£10', '£25',
                    '£50', '£100', '£1000']
    current_game_speed = 'Normal'
    game_delay = 1000
    game_in_play = False
    game_speed = ['Slow', 'Normal', 'Fast']
    high_score = 100
    hits = 0
    keno_numbers = list(range(1, 81))
    matched_numbers = 0
    not_enough_cash = False
    payout_dict = {}
    payout_frame = None
    payout_label = None
    picked_numbers = []
    players_stake = 1
    players_bank = 100
    previous_selections = []
    rnd_selecs = ['OFF', 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    selections = 0
    tiles = []
    total_payout = 0
    win_multiplier = 0


def high_score_file_check():
    """ Check for existance of high score text file,
        if not exist then create one. """
    filename = 'data/high_score.txt'
    if os.path.isfile(filename):
        return
    else:
        with open(filename, "w") as f:
            f.write('100')


high_score_file_check()


def load_high_score():
    """ Load back the high score variable from file
        and store in Fs.high_score."""
    with open(r'data/high_score.txt', 'r') as contents:
        stored_high_score = contents.read()
        if stored_high_score > '':
            Fs.high_score = int(stored_high_score)


load_high_score()


def save_high_score():
    """ Save current score to file if it beats previous highscore."""
    if Fs.players_bank < Fs.high_score:
        return

    with open(r'data/high_score.txt', 'w') as contents:
        save_it = str(Fs.players_bank)
        contents.write(save_it)


def update_high_score():
    """ Update high score label. """
    if Fs.players_bank > Fs.high_score:
        Fs.high_score = Fs.players_bank
        high_score_label.config(text='HIGH SCORE £'+str(Fs.high_score))
        save_high_score()


def help_text_check():
    """ Check for existance of help text file,
        if not exist then disable help menu item. """
    file_name = 'data/keno_help.txt'
    if os.path.isfile(file_name):
        return
    # disable help menu item
    file_menu.entryconfig("Help", state="disabled")
    messagebox.showinfo('Keno Sim Program Information',
                        'The file keno_help.txt is missing\n'
                        'from the data folder, so I have\n'
                        'disabled help in the menu.\n'
                        'Just saying.')


def check_logo():
    """ Check for existance of logo image file. """
    file_name = r'data/keno-sim-logo.png'
    if os.path.isfile(file_name):
        return

    messagebox.showinfo('Keno Sim Program Information',
                        'The file data/keno-sim-logo.png is missing\n'
                        'Please fix or re-install program.\n')
    root.destroy()
    sys.exit()


check_logo()


def check_sfx():
    """ Check sfx folder and wav files present. """
    file_names = ['keno_ball.wav', 'keno_got_a_win.wav',
                  'keno_hit.wav', 'keno_intro.wav', 'keno_lost.wav']
    for file_name in file_names:
        try:
            with open(os.path.join(r'data/sfx/', file_name), 'rb') as f:
                pass
        except IOError:
            messagebox.showinfo('Keno Sim Program Information',
                            'The file ' +str(file_name) +' is missing\n'
                            'Please fix or re-install program.\n')
            root.destroy()
            sys.exit()


check_sfx()


def new_game():
    """ Set up for a new game. """
    # reset vars
    update_high_score()
    clear_all()
    Fs.hits = 0
    Fs.matched_numbers = 0
    total_payout = 0
    win_multiplier = 0
    picked_numbers = []

    # reset buttons
    stake_combo.config(state='normal')
    rnd_combo.config(state='normal')
    clear_btn.config(state='normal')
    new_game_btn.config(state='disabled')

    # clear hits and wins
    hits_and_wins_label.config(text='')

    Fs.ball_numb_lab.config(text='KENO')
    Fs.call_counter_lab.config(text='  Call 0 OF 20    ')


def play_sound(filename):
    """ Play WAV file.Supply filename when calling this function. """
    data, fs = sf.read(filename, dtype='float32')
    sd.play(data, fs)


def payout_tables():
    """ Payout tables for display during game dependent
        on the amount of selections, 3 to 15. """
    Fs.payout_dict = {
        3: {'03 HITS': '48 x stake', '02 HITS': '2 x stake',
            '01 HITS ': '0 x stake', '00 HITS': '0 x stake'},

        4: {'04 HITS': '65 x stake', '03 HITS': '10 x stake',
            '02 HITS': '2 x stake', '01 HITS ': '0 x stake',
            '00 HITS': '0 x stake'},

        5: {'05 HITS': '100 x stake', '04 HITS': '12 x stake',
            '03 HITS': '4 x stake', '02 HITS': '1 x stake',
            '01 HITS ': '0 x stake', '00 HITS': '0 x stake'},

        6: {'06 HITS': '200 x stake', '05 HITS': '44 x stake',
            '04 HITS': '10 x stake', '03 HITS': '1 x stake',
            '02 HITS': '1 x stake', '01 HITS': '0 x stake',
            '00 HITS': '0 x stake'},

        7: {'07 HITS': '300 x stake', '06 HITS': '100 x stake',
            '05 HITS': '24 x stake', '04 HITS': '6 x stake',
            '03 HITS': '2 x stake', '02 HITS': '0 x stake',
            '01 HITS ': '0 x stake', '00 HITS': '0 x stake'},

        8: {'08 HITS': '1000 x stake', '07 HITS': '500 x stake',
            '06 HITS': '60 x stake', '05 HITS': '10 x stake',
            '04 HITS': '4 x stake', '03 HITS': '1 x stake',
            '02 HITS': '0 x stake', '01 HITS ': '0 x stake',
            '00 HITS': '0 x stake'},

        9: {'09 HITS': '2000 x stake', '08 HITS': '400 x stake',
            '07 HITS': '50 x stake', '06 HITS': '20 x stake',
            '05 HITS': '8 x stake', '04 HITS': '3 x stake',
            '03 HITS': '1 x stake', '02 HITS': '0 x stake',
            '01 HITS ': '0 x stake', '00 HITS': '0 x stake'},

        10: {'10 HITS': '3000 x stake', '09 HITS': '500 x stake',
             '08 HITS': '100 x stake', '07 HITS': '32 x stake',
             '06 HITS': '10 x stake', '05 HITS': '4 x stake',
             '04 HITS': '2 x stake', '03 HITS': '1 x stake',
             '02 HITS': '0 x stake', '01 HITS ': '0 x stake',
             '00 HITS': '0 x stake'},

        11: {'11 HITS': '4000 x stake', '10 HITS': '1000 x stake',
             '09 HITS': '600 x stake', '08 HITS': '70 x stake',
             '07 HITS': '20 x stake', '06 HITS': '10 x stake',
             '05 HITS': '4 x stake', '04 HITS': '1 x stake',
             '03 HITS': '0 x stake', '02 HITS': '0 x stake',
             '01 HITS ': '0 x stake', '00 HITS': '2 x stake'},

        12: {'12 HITS': '5000 x stake', '11 HITS': '2000 x stake',
             '10 HITS': '800 x stake', '09 HITS': '300 x stake',
             '08 HITS': '50 x stake', '07 HITS': '20 x stake',
             '06 HITS': '5 x stake', '05 HITS': '2 x stake',
             '04 HITS': '1 x stake', '03 HITS': '0 x stake',
             '02 HITS': '0 x stake', '01 HITS': '1 x stake',
             '00 HITS': '2 x stake'},

        13: {'13 HITS': '6000 x stake', '12 HITS': '3000 x stake',
             '11 HITS': '1500 x stake', '10 HITS': '500 x stake',
             '09 HITS': '50 x stake', '08 HITS': '20 x stake',
             '07 HITS': '10 x stake', '06 HITS': '3 x stake',
             '05 HITS': '2 x stake', '04 HITS': '1 x stake',
             '03 HITS': '0 x stake', '02 HITS': '0 x stake',
             '01 HITS ': '1 x stake', '00 HITS': '3 x stake'},

        14: {'14 HITS': '8000 x stake', '13 HITS': '4000 x stake',
             '12 HITS': '1500 x stake', '11 HITS': '1000 x stake',
             '10 HITS': '150 x stake', '09 HITS': '50 x stake',
             '08 HITS': '16 x stake', '07 HITS': '8 x stake',
             '06 HITS': '4 x stake', '05 HITS': '2 x stake',
             '04 HITS': '0 x stake', '03 HITS': '0 x stake',
             '02 HITS': '0 x stake', '01 HITS ': '2 x stake',
             '00 HITS': '4 x stake'},

        15: {'15 HITS': '9999 x stake', '14 HITS': '5000 x stake',
             '13 HITS': '3000 x stake', '12 HITS': '1500 x stake',
             '11 HITS': '500 x stake', '10 HITS': '100 x stake',
             '09 HITS': '25 x stake', '08 HITS': '8 x stake',
             '07 HITS': '5 x stake', '06 HITS': '3 x stake',
             '05 HITS': '2 x stake', '04 HITS': '0 x stake',
             '03 HITS': '0 x stake', '02 HITS': '0 x stake',
             '01 HITS ': '2 x stake', '00 HITS': '4 x stake'}
    }

    num_picked = len(Fs.picked_numbers)

    # I got chatgpt to write this bit of code below, out of my ability.
    if num_picked in Fs.payout_dict:
        payout_table = Fs.payout_dict[num_picked]

        max_key_width = max(len(key) for key in payout_table.keys())
        max_value_width = max(len(value) for value in payout_table.values())
        text = '\n'.join([f'{key:<{max_key_width}s} {value:>{max_value_width}s}'
                          for key, value in payout_table.items()])

        Fs.payout_label.config(font=cfont, text=text)
        Fs.payout_frame.config(text='Payout Table')


def update_bank():
    """ Update bank label. """
    temp_text = 'Bank:£'+str(Fs.players_bank)
    bank_lab.config(text=temp_text)


def check_if_win():
    """ Check if player has won a prize according to selections and hits."""
    Fs.win_multiplier = 0

    payouts = {
        (3, 2): 2,
        (3, 3): 48,

        (4, 2): 2,
        (4, 3): 10,
        (4, 4): 65,

        (5, 2): 1,
        (5, 3): 4,
        (5, 4): 12,
        (5, 5): 100,

        (6, 2): 1,
        (6, 3): 1,
        (6, 4): 10,
        (6, 5): 44,
        (6, 6): 200,

        (7, 3): 2,
        (7, 4): 6,
        (7, 5): 24,
        (7, 6): 100,
        (7, 7): 300,

        (8, 3): 1,
        (8, 4): 4,
        (8, 5): 10,
        (8, 6): 60,
        (8, 7): 500,
        (8, 8): 1000,

        (9, 3): 1,
        (9, 4): 3,
        (9, 5): 8,
        (9, 6): 20,
        (9, 7): 50,
        (9, 8): 400,
        (9, 9): 2000,

        (10, 3): 1,
        (10, 4): 2,
        (10, 5): 4,
        (10, 6): 10,
        (10, 7): 32,
        (10, 8): 100,
        (10, 9): 500,
        (10, 10): 3000,

        (11, 0): 2,
        (11, 4): 1,
        (11, 5): 4,
        (11, 6): 10,
        (11, 7): 20,
        (11, 8): 70,
        (11, 9): 600,
        (11, 10): 1000,
        (11, 11): 4000,

        (12, 0): 2,
        (12, 1): 1,
        (12, 4): 1,
        (12, 5): 2,
        (12, 6): 5,
        (12, 7): 20,
        (12, 8): 50,
        (12, 9): 300,
        (12, 10): 800,
        (12, 11): 2000,
        (12, 12): 5000,

        (13, 0): 3,
        (13, 1): 1,
        (13, 4): 1,
        (13, 5): 2,
        (13, 6): 3,
        (13, 7): 10,
        (13, 8): 20,
        (13, 9): 50,
        (13, 10): 500,
        (13, 11): 1500,
        (13, 12): 3000,
        (13, 13): 6000,

        (14, 0): 4,
        (14, 1): 2,
        (14, 5): 2,
        (14, 6): 4,
        (14, 7): 8,
        (14, 8): 16,
        (14, 9): 50,
        (14, 10): 150,
        (14, 11): 1000,
        (14, 12): 1500,
        (14, 13): 4000,
        (14, 14): 8000,

        (15, 0): 4,
        (15, 1): 2,
        (15, 5): 2,
        (15, 6): 3,
        (15, 7): 5,
        (15, 8): 8,
        (15, 9): 25,
        (15, 10): 100,
        (15, 11): 500,
        (15, 12): 1500,
        (15, 13): 3000,
        (15, 14): 5000,
        (15, 15): 9999,
        }

    Fs.selections = len(Fs.picked_numbers)
    Fs.win_multiplier = payouts.get((Fs.selections, Fs.hits), 0)
    Fs.total_payout = Fs.win_multiplier * Fs.players_stake

    result = 'Selections:' + str(Fs.selections) +  \
             '  Hits:' + str(Fs.hits) +  \
             '\nStake £' + str(Fs.players_stake) +  \
             '   Prize £' + str(Fs.total_payout)

    # Update label with result info
    hits_and_wins_label.config(fg='green',
                               font=('Arial', 10, 'bold'),
                               text=result)

    if Fs.win_multiplier:
        play_sound(r'data/sfx/keno_got_a_win.wav')
    else:
        play_sound(r'data/sfx/keno_lost.wav')

    # Credit winnings to players bank
    Fs.players_bank += Fs.total_payout
    update_bank()
    update_high_score()
    new_game_btn.config(state='normal')


def no_selections_payout_msg():
    """ Start up text in payout window. """
    payout_msg = 'This game is a simulation of an online\n'  \
                 'Keno game that I play.\n'  \
                 'I made this to test strategies\n'  \
                 'and compare results to see\n'  \
                 'how the online game matched up\n\n'  \
                 '\nSelect your stake.\n\nClick on 3 to 15 numbered boxes,\n\n'  \
                 'or use the random drop-down menu,\n\nSelect game speed,\n\n'  \
                 'and then click "Play".\n\n'  \
                 'Click "New Game" or "Repeat Last Bet"\n'  \
                 'buttons to play another game\n\n'  \
                 'This game is random.\n'  \
                 'RTP is approximately 95%-96%\n\n'  \
                 '(c) Steve Shambles April 2023'
    Fs.payout_label.config(font=('times', 10, 'bold'), text=payout_msg)


def clear_all():
    """ Clear all relevant vars ready for a new game. """
    Fs.picked_numbers = []
    matched_numbers = 0
    Fs.payout_frame.config(text='Keno Instructions')
    Fs.payout_label.config(text='')
    hits_and_wins_label.config(text='')
    # Clear button states.
    for i in range(1, 81):
        if Fs.tiles[i].cget("state") == "disabled":
            Fs.tiles[i].config(state="normal", bg='powderblue')
    no_selections_payout_msg()
    play_btn.config(state='disabled')


def button_click(number):
    """ Let user pick numbers, or random pick. """
    if Fs.game_in_play:
        return
    if len(Fs.picked_numbers) >= 15:
        return
    if len(Fs.picked_numbers) > 1:
        play_btn.config(state='normal')

    # save users number picks from previous game or [] if first game.
    Fs.previous_selections = Fs.picked_numbers

    if number not in Fs.picked_numbers:
        Fs.tiles[number].config(state="disabled", bg='gold')
        Fs.picked_numbers.append(number)
        # save users number picks from previous game or [] if first game.
        Fs.previous_selections = Fs.picked_numbers

    for i in range(3, 16):
        if len(Fs.picked_numbers) == i:
            payout_tables()


def create_rnd_numbs(amount):
    """ Program picks user defined amount of rnd numbers. """
    Fs.picked_numbers = []
    clear_all()
    while len(Fs.picked_numbers) < amount:
        rnd_num = random.randint(1, 80)
        if rnd_num not in Fs.picked_numbers:
            button_click(rnd_num)

    return (Fs.picked_numbers)


def random_combo_event(event):
    """ Comes here when a selection from the rnd combo box is made."""

    # how many selections has user picked from combo?
    try:
        Fs.amount_of_user_selections = int(event.widget.get())
    except:
        # user selected OFF
        rnd_combo.current(0)
        clear_all()
        return

    # Call random number gen
    create_rnd_numbs(Fs.amount_of_user_selections)

    Fs.selections = Fs.amount_of_user_selections
    # display the payout table for that selection
    payout_tables()

    # light up play btn ready to play game.
    play_btn.config(state='normal')

    # Update selections combo
    temp_us = Fs.amount_of_user_selections
    temp_us -= 2
    rnd_combo.current(temp_us)


def not_enough_cash():
    """ Player has run out of money. """
    msg = ''
    if Fs.players_bank <= 0:
        msg = 'Please reload game and try again.'

    messagebox.showinfo('Oh no! ',
                        'You do not have enough\n'
                        'money to to place that bet.\n\n' +
                        str(msg))


def stake_combo_event(event):
    """ Players stake selection. """
    # Check enough in players bank to make bet.
    temp_stake = event.widget.get()
    temp_players_stake = temp_stake.replace("£", "")

    Fs.not_enough_cash = False
    if int(Fs.players_bank) < int(temp_players_stake):
        Fs.not_enough_cash = True
        not_enough_cash()
        return

    Fs.players_stake = int(temp_players_stake)


def game_speed_control():
    """ Game speed control. """
    if Fs.current_game_speed == 'Slow':
        Fs.game_delay = 2000
    if Fs.current_game_speed == 'Normal':
        Fs.game_delay = 1000
    if Fs.current_game_speed == 'Fast':
        Fs.game_delay = 10


def game_speed_event(event):
    """ Get currently selected game speed. """
    Fs.current_game_speed = event.widget.get()
    game_speed_control()


def button_click_handler(event):
    """ Get the number of the clicked button from its label. """
    if Fs.game_in_play:
        return
    number = int(event.widget['text'])
    button_click(number)


def check_hit():
    """ If a match, then bg color tile green, if number not a hit,
        then colour tile red. """
    if int(Fs.called_number) in Fs.picked_numbers:
        Fs.tiles[int(Fs.called_number)].config(bg='limegreen')
        play_sound(r'data/sfx/keno_hit.wav')
        Fs.matched_numbers += 1
        Fs.hits += 1
    else:
        Fs.tiles[int(Fs.called_number)].config(state="disabled",
                                               bg='indianred')
        play_sound(r'data/sfx/keno_ball.wav')


def game_over():
    """ If game over."""
    Fs.keno_numbers = list(range(1, 81))
    repeat_btn.config(state='normal')


def choose_number():
    """ Grab a random number 1-80, 20 times.
        Fs.called_number is the current random number in the
        loop of 20 calls"""

    if Fs.call_count < 20:
        if Fs.keno_numbers:
            # Choose a random number from the list
            number = random.choice(Fs.keno_numbers)
            # Remove the chosen number from the list
            Fs.keno_numbers.remove(number)
            # Pad single digits with a zero to their left
            Fs.called_number = str(number).zfill(2)
            # Display the chosen number in the tkinter window
            Fs.ball_numb_lab.config(text='  ' + str(Fs.called_number) + '  ')
            # show counter
            temp_cc = Fs.call_count + 1
            counter_digit = str(temp_cc).zfill(2)
            count_msg = 'Call ' + str(counter_digit) + ' OF ' + '20'
            Fs.call_counter_lab.config(text=(count_msg))
        # Increment the counter variable
        Fs.call_count += 1

        check_hit()

        root.after(Fs.game_delay, choose_number)

    else:
        check_if_win()
        game_over()


def play_keno():
    """ Starts the actual number calling part of the game. """
    if Fs.not_enough_cash:
        not_enough_cash()
        return
    # extra check needed for other circs.
    if Fs.players_stake > Fs.players_bank:
        not_enough_cash()
        return
    # disable necessary widgets
    stake_combo.config(state='disabled')
    rnd_combo.config(state='disabled')
    clear_btn.config(state='disabled')
    play_btn.config(state='disabled')

    Fs.game_in_play == True
    # take stake money from players bank
    Fs.players_bank = Fs.players_bank - int(Fs.players_stake)
    update_bank()
    game_speed_control()
    Fs.call_count = 0
    choose_number()  # start calling numbers


def repeat_last_bet():
    """ Repeat last bet btn clicked, have to account for random
        sels and manual type selections and careful not to
        zero certain vars"""
    if Fs.players_bank - Fs.players_stake < 0:
        not_enough_cash()
        repeat_btn.config(state='disabled')
        return

    Fs.call_count = 0
    Fs.win_multiplier = 0
    Fs.total_payout = 0
    Fs.matched_numbers = 0
    Fs.hits = 0
    called_number = 0
    clicked_buttons = []
    tiles = []
    hits_and_wins_label.config(text='')
    Fs.amount_of_user_selections = len(Fs.picked_numbers)
    # reset keno number list to repopulate previously removed numbers
    keno_numbers = list(range(1, 81))
    # Clear board.
    for i in range(1, 81):
        if Fs.tiles[i].cget("state") == "disabled":
            Fs.tiles[i].config(state="normal", bg='powderblue')
    # now fill board with previous games selected numbers
    for i in range(Fs.amount_of_user_selections):
        number = int(Fs.previous_selections[i])
        Fs.tiles[number].config(state="disabled", bg='gold')

    stake_combo.config(state='disabled')
    rnd_combo.config(state='disabled')
    clear_btn.config(state='disabled')
    repeat_btn.config(state='disabled')
    new_game_btn.config(state='disabled')
    play_btn.config(state='normal')


def help_text():
    """ Show help text file. """
    web.open(r'data\keno_help.txt')


def about_menu():
    """ About program msgbox. """
    messagebox.showinfo('Keno Sim Program Information',
                        'Keno Simulator V1\n\n'
                        'Freeware by Steve Shambles\n'
                        'Source code MIT Licence.\n'
                        'See help file for more details.\n\n'
                        '(c) April 2023\n')


def donate_me():
    """ User splashes the cash here! """
    web.open('https:\\paypal.me/photocolourizer')


def visit_github():
    """ View source code and my other Python projects at GitHub. """
    web.open('https://github.com/Steve-Shambles?tab=repositories')


def exit_keno():
    """ Yes-no requestor to exit program. """
    ask_yn = messagebox.askyesno('Question',
                                 'Quit Keno Sim?')
    if ask_yn is False:
        return
    root.destroy()
    sys.exit()


# start up music
play_sound(r'data/sfx/keno_intro.wav')

# Insert logo.
logo_frame = tk.LabelFrame(root)
logo_image = Image.open(r'data/keno-sim-logo.png')
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(logo_frame, image=logo_photo)
logo_label.logo_image = logo_photo
logo_label.grid()
logo_frame.grid(padx=7)

# Create 80 buttons arranged in a 10x8 grid, with zero-padded labels
tiles_frame = tk.Frame(root)
Fs.tiles = {}
for row in range(8):
    for col in range(10):
        i = row * 10 + col + 1
        label = '{:02d}'.format(i)
        button = tk.Button(tiles_frame, font=('helvetica', 14, 'bold'),
                           bg='powderblue', fg='darkblue', text=label)
        button.grid(row=row, column=col)
        button.bind("<Button-1>", button_click_handler)
        Fs.tiles[i] = button
tiles_frame.grid(row=5, column=0, padx=8, rowspan=8, columnspan=10)


btn_frame = tk.Frame(root)
# stake label
stake_lab = tk.Label(btn_frame, fg='blue',
                     font=cfont, text='Stake:')
stake_lab.grid(row=0, column=0)

# Random label
rnd_lab = tk.Label(btn_frame, fg='blue',
                   font=cfont, text='Random:')
rnd_lab.grid(row=0, column=1)

# speed label
speed_lab = tk.Label(btn_frame, fg='blue',
                     font=cfont, text='Speed:')
speed_lab.grid(row=0, column=2)

# Players Bank label
bank_lab = tk.Label(btn_frame,
                    font=cfont, text='Bank:')
bank_lab.grid(row=0, column=4, sticky='e')
update_bank()

# stake combo
stake_combo = ttk.Combobox(btn_frame, width=5,
                           values=Fs.combo_stakes)
stake_combo.grid(row=1, column=0, padx=8)
stake_combo.configure(state="readonly")
stake_combo.current(0)

# rnd combo box
rnd_combo = ttk.Combobox(btn_frame, width=5,
                         values=Fs.rnd_selecs)
rnd_combo.grid(row=1, column=1, padx=8)
rnd_combo.current(0)
rnd_combo.configure(state="readonly")

# Speed combo box
speed_combo = ttk.Combobox(btn_frame, width=6,
                           values=Fs.game_speed)
speed_combo.grid(row=1, column=2, padx=8)
speed_combo.current(1)
speed_combo.configure(state="readonly")

# buttons
clear_btn = tk.Button(btn_frame, bg='gold',
                      text='     Clear     ',
                      command=clear_all)
clear_btn.grid(row=1, column=3, pady=8, padx=4)

play_btn = tk.Button(btn_frame, bg='limegreen',
                     text='     Play     ',
                     command=play_keno)
play_btn.grid(row=1, column=4)
play_btn.config(state='disabled')

btn_frame.grid(row=14, column=0, columnspan=12)

# frame for payout tables
temp_txt = 'Keno Sim Instructions'
Fs.payout_frame = tk.LabelFrame(root, fg='navyblue',
                                text=temp_txt)
Fs.payout_label = tk.Label(Fs.payout_frame, bg='gold')
Fs.payout_label.grid(row=4, column=0)
Fs.payout_frame.grid(row=0, column=10, rowspan=8,
                     columnspan=25, padx=12)

no_selections_payout_msg()

# frame for in game display of hits and final winnings if any
hits_and_wins_frame = tk.LabelFrame(root, fg='indianred',
                                    font=('Arial', 9, 'bold'),
                                    text='                   Hits and Wins                 ')
hits_and_wins_label = tk.Label(hits_and_wins_frame)

hits_and_wins_label.grid(row=4, column=0, columnspan=18)

hits_and_wins_frame.grid(row=14, column=10, rowspan=12,
                         columnspan=25, padx=12)


repeat_btn = tk.Button(hits_and_wins_frame, bg='white',
                       text='Repeat Last Bet',
                       command=repeat_last_bet)
repeat_btn.grid(row=5, column=5, padx=12)
repeat_btn.config(state='disabled')

new_game_btn = tk.Button(hits_and_wins_frame, bg='white',
                         text=' New  Game ',
                         command=new_game)
new_game_btn.grid(row=5, column=6, padx=12)
new_game_btn.config(state='disabled')


high_score_label = tk.Button(hits_and_wins_frame, bg='white',
                             text='HIGH SCORE £'+str(Fs.high_score))
high_score_label.grid(row=6, column=0, padx=6, columnspan=10)
high_score_label.config(state='disabled')

# Call counter frame and label
Fs.call_counter_frame = tk.LabelFrame(root, bg='orange')
Fs.call_counter_lab = tk.Label(Fs.call_counter_frame, bg='orange',
                               font=('Arial', 24),
                               text='  Call 0 OF 20')
Fs.call_counter_lab.grid(row=0, column=10, columnspan=10, padx=12)
Fs.call_counter_frame.grid(row=16, column=0, columnspan=10,
                           padx=12, sticky='we')

# Create frame and label to display the chosen number during game
Fs.ball_numb_lab = tk.Label(Fs.call_counter_frame, bg='blue',
                            fg='white', font=('Arial', 24),
                            text='KENO')
Fs.ball_numb_lab.grid(row=0, column=0, columnspan=10, padx=12)

# bind combo boxes so auto-detect changes
rnd_combo.bind("<<ComboboxSelected>>", random_combo_event)
stake_combo.bind("<<ComboboxSelected>>", stake_combo_event)
speed_combo.bind("<<ComboboxSelected>>", game_speed_event)


# Pre-load icons for drop-down menu.
try:
    help_icon = ImageTk.PhotoImage(file=r'data/icons/help-16x16.ico')
    about_icon = ImageTk.PhotoImage(file=r'data/icons/about-16x16.ico')
    exit_icon = ImageTk.PhotoImage(file=r'data/icons/exit-16x16.ico')
    donation_icon = ImageTk.PhotoImage(file=r'data/icons/donation-16x16.ico')
    github_icon = ImageTk.PhotoImage(file=r'data/icons/github-16x16.ico')
except FileNotFoundError:
    messagebox.showinfo('Keno Sim Program Information',
                        'There was an error\n'
                        'Icons are missing from the data folder\n'
                        'Please fix or re-install')
    root.destroy()
    sys.exit()

# Menu
menu_bar = Menu(root)
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Menu', menu=file_menu)

file_menu.add_command(label='Help', compound='left',
                      image=help_icon, command=help_text)
file_menu.add_command(label='About', compound='left',
                      image=about_icon, command=about_menu)
file_menu.add_separator()
file_menu.add_command(label='Python source code on GitHub', compound='left',
                      image=github_icon, command=visit_github)
file_menu.add_command(label='Make a small donation via PayPal',
                      compound='left',
                      image=donation_icon, command=donate_me)
file_menu.add_separator()
file_menu.add_command(label='Exit', compound='left',
                      image=exit_icon, command=exit_keno)
root.config(menu=menu_bar)

help_text_check()

root.eval('tk::PlaceWindow . Center')
root.protocol('WM_DELETE_WINDOW', exit_keno)


root.mainloop()
