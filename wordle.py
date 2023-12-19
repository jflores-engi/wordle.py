import random
import os
import nltk
import json

game_historical_data = []
data_filename = 'wordle_data.txt'
game_session_data = []

try: 
    with open(data_filename) as data_file:
        game_historical_data = json.load(data_file)
except Exception:
    'File not found'

###########################################################################

class Game_Data:
    def __init__(self, correct_word, win, attempts, guesses):
        self.correct_word = correct_word
        self.win = win
        self.attempts = attempts
        self.guesses = guesses

###########################################################################


word_list = [word for word in nltk.corpus.words.words() if len(word)==5 and word.isalpha()]

def generate_word():
    return random.choice(word_list)

def check_guess(word, guess):
    if len(guess) != len(word):
        return False
    
    for i in range(len(word)):
        if guess[i] == word[i]:
            print(f"{guess[i]}", end=" ")
        elif guess[i] in word:
            print("_", end=" ")
        else:
            print("*", end=" ")
    
    print()
    return guess == word

def play_wordle():
    word = generate_word()
    attempts = 0
    guess_list = []
    win = False
    
    print("Welcome to Wordle!")
    print("Guess the word by entering words of the same length.")
    print("Each correct letter in the right position will be shown as the letter itself.")
    print("Each correct letter in the wrong position will be shown as an underscore (_).")
    print("Each incorrect letter will be shown as an asterisk (*).")
    print("Type exit to save and quit")
    
    while attempts < 5:
        guess = '-'
        while (not (guess.isalpha() and len(guess)==5 and (guess not in guess_list))) or guess.lower()=='exit':
            guess = input("Enter your guess: ").lower()
            if guess.lower() == 'exit':
                with open(data_filename) as data_file:
                    json.dump(game_historical_data+game_session_data,data_file)
                    exit()
            elif len(guess) != 5:
                print('Invalid length of guess, must be exactly 5 letters')
            elif guess in guess_list:
                print(f"'{guess}' has already been guessed.")
        guess_list.append(guess)
        attempts += 1
        
        if check_guess(word, guess):
            os.system('cls')
            print(f"Congratulations! You guessed the word '{word}' in {attempts} attempts.")
            win = True
            break
    if attempts == 5:
        print(f"The correct answer was '{word}'.")
    print("Thanks for playing!")
    print('\n\n')
    print("="*100)
    print('\n\n')

    game_data = Game_Data(word,win,attempts,guess_list)
    game_session_data.append(game_data)

# close loop out of play_wordle and export data

while True:
    play_wordle()

# FIX: if multiple of the same letter are correct, it should only show as many as there are in the word

# TODO: show number of guesses left.
# TODO: 'show_stats' command
# TODO: 'define' command
# TODO: create statistical metrics based on saved game data
# TODO: Do statistical determination of word-complexity/difficulty based on:
#  - How common each letter is
#  - How common the word is

