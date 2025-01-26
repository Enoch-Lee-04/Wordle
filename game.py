"""Module providing a simple word game called Wordle."""

import sys
import random
import csv
import pygame
#from words import *

pygame.init()

# load words from the CSV file
def load_words_from_csv(filepath):
    words = []
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            words.append(row[0])
    return words

words = load_words_from_csv('assets/FreqWords.csv')

# Constants

WIDTH, HEIGHT = 633, 900

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND = pygame.image.load("assets\Starting Tiles.png")
BACKGROUND_RECT = BACKGROUND.get_rect(center=(317, 300))
ICON = pygame.image.load("assets\Icon.png")

pygame.display.set_caption("Wordle")
pygame.display.set_icon(ICON)

GREEN = "#6aaa64"
YELLOW = "#c9b458"
GRAY = "#787c7e"
OUTLINE = "#d3d6da"
FILLED_OUTLINE = "#878a8c"

CORRECT_WORD = random.choice(words).lower()

ALPHABET = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

GUESSED_LETTER_FONT = pygame.font.Font("assets/FreeSansBold.otf", 50)
AVAILABLE_LETTER_FONT = pygame.font.Font("assets/FreeSansBold.otf", 25)

SCREEN.fill("white")
SCREEN.blit(BACKGROUND, BACKGROUND_RECT)
pygame.display.update()

LETTER_X_SPACING = 85
LETTER_Y_SPACING = 12
LETTER_SIZE = 75

GUESSES_COUNT = 0

# guess is a 2D list that will store user's guesses. A guess will contain list of letters.
# the list will be iterated over and each letter in each guess
guesses = [[]] * 6

current_guess = []
current_guess_string = ""
current_letter_bg_x = 109

# a list storing all the letter object with a button with all the letters you can click
letters = []

GAME_RESULT = ""

message_display_time = 0 # time whe the message was displayed
MESSAGE_DISPLAY_DURATION = 2500 # duration of the message display

class Letter:
    def __init__(self, text, bg_position):
        # initializes the letter object
        self.text = text
        self.bg_position = bg_position
        self.bg_color = "white"
        self.text_color = "black"
        self.bg_x = bg_position[0]
        self.bg_y = bg_position[1]
        self.bg_rect = (bg_position[0], self.bg_y, LETTER_SIZE, LETTER_SIZE)
        self.position = (self.bg_x + 36, self.bg_position[1] + 34)
        self.text_surface = GUESSED_LETTER_FONT.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.position)

    def draw(self):
        # puts the letter and text on the correct position on the screen
        pygame.draw.rect(SCREEN, self.bg_color, self.bg_rect)
        if self.bg_color == "white":
            pygame.draw.rect(SCREEN, FILLED_OUTLINE, self.bg_rect, 3)
        self.text_surface = GUESSED_LETTER_FONT.render(self.text, True,self.text_color)
        SCREEN.blit(self.text_surface, self.text_rect)
        pygame.display.update()

    def delete(self):
        # fills the letter's spot with the default square, and resets the text and text color
        pygame.draw.rect(SCREEN, "white", self.bg_rect)
        pygame.draw.rect(SCREEN, OUTLINE, self.bg_rect, 3)
        pygame.display.update()

class Keyboard:
    def __init__(self, x, y, letter):
        # initializes the indicator object
        self.x = x
        self.y = y
        self.text = letter
        self.rect = (self.x, self.y, 57, 75)
        self.bg_color = OUTLINE

    def draw(self):
        # puts the indicator and its text on the correct position on the screen
        pygame.draw.rect(SCREEN, self.bg_color, self.rect)
        self.text_surface = AVAILABLE_LETTER_FONT.render(self.text, True, "white")
        self.text_rect = self.text_surface.get_rect(center=(self.x + 27, self.y + 30))
        SCREEN.blit(self.text_surface, self.text_rect)
        pygame.display.update()

# drawing the keyboards on the screen
keyboard_x, keyboard_y = 20, 600

for i in range(3):
    for letter in ALPHABET[i]:
        keyboard = Keyboard(keyboard_x, keyboard_y, letter)
        letters.append(keyboard)
        keyboard.draw()
        keyboard_x += 60
    keyboard_y += 100 # moves the keyboard row down
    if i == 0:
        keyboard_x = 50
    elif i == 1:
        keyboard_x = 105

def check_guess(guess_to_check):
    # checks the guess and updates uers' guess with the correct colors
    global current_guess, current_guess_string, GUESSES_COUNT, current_letter_bg_x, GAME_RESULT
    game_decided = False

    for i in range(5):
        lowercase_letter = guess_to_check[i].text.lower()
        if lowercase_letter in CORRECT_WORD: # if the letter is in the correct word
            if lowercase_letter == CORRECT_WORD[i]: # if the letter is in the correct position
                guess_to_check[i].bg_color = GREEN
                for indicator in letters:
                    if indicator.text == lowercase_letter.upper():
                        indicator.bg_color = GREEN
                        indicator.draw()
                guess_to_check[i].text_color = "white" # if the background is green, than the text should be white
                if not game_decided:
                    GAME_RESULT = "W"
            else: # letter is in the word but not in the correct position
                guess_to_check[i].bg_color = YELLOW
                for indicator in letters:
                    if indicator.text == lowercase_letter.upper():
                        indicator.bg_color = YELLOW
                        indicator.draw()
                guess_to_check[i].text_color = "white"
                GAME_RESULT = ""
                game_decided = True
        else: # letter is not in the word
            guess_to_check[i].bg_color = GRAY
            for indicator in letters:
                if indicator.text == lowercase_letter.upper():
                    indicator.bg_color = GRAY
                    indicator.draw()
            guess_to_check[i].text_color = "white"
            GAME_RESULT = ""
            game_decided = True
        # draw the letter on the screen
        guess_to_check[i].draw()
        pygame.display.update()

    GUESSES_COUNT += 1
    current_guess = []
    current_guess_string = ""
    current_letter_bg_x = 109

    if GUESSES_COUNT == 6 and GAME_RESULT == "":
        GAME_RESULT = "L"

def play_again():
    # puts the play again text on the screen
    pygame.draw.rect(SCREEN, "white", (10, 600, 1000, 600))
    play_again_font = pygame.font.Font("assets/FreeSansBold.otf", 40)
    play_again_text = play_again_font.render("Press ENTER to play again!", True, "black")
    play_again_rect = play_again_text.get_rect(center = (WIDTH/2, 700))
    word_was_text = play_again_font.render(f"The word was {CORRECT_WORD.upper()}", True, "black")
    word_was_rect = word_was_text.get_rect(center = (WIDTH/2, 650))
    SCREEN.blit(word_was_text, word_was_rect)
    SCREEN.blit(play_again_text, play_again_rect)
    pygame.display.update()

def reset():
    # resets all variables to their default states
    global GUESSES_COUNT, CORRECT_WORD, guesses, current_guess, current_guess_string, GAME_RESULT
    SCREEN.fill("white")
    SCREEN.blit(BACKGROUND, BACKGROUND_RECT)
    GUESSES_COUNT = 0
    CORRECT_WORD = random.choice(words).lower()
    guesses = [[]] * 6
    current_guess = []
    current_guess_string = ""
    GAME_RESULT = ""
    pygame.display.update()
    for indicator in letters:
        indicator.bg_color = OUTLINE
        indicator.draw()

def create_new_letter(key_pressed):
    # creates a new letter and adds it to the guess
    global current_guess_string, current_letter_bg_x
    current_guess_string += key_pressed
    new_letter = Letter(key_pressed, (current_letter_bg_x, GUESSES_COUNT * 100 + LETTER_Y_SPACING))
    current_letter_bg_x += LETTER_X_SPACING
    guesses[GUESSES_COUNT].append(new_letter)
    current_guess.append(new_letter)

    for guess in guesses:
        for letter in guess:
            letter.draw()

def delete_letter():
    # deletes a letter from the screen
    global current_guess_string, current_letter_bg_x
    guesses[GUESSES_COUNT][-1].delete()
    guesses[GUESSES_COUNT].pop() # removes letter from the guess list
    current_guess_string = current_guess_string[:-1]
    current_guess.pop()
    current_letter_bg_x -= LETTER_X_SPACING

def redraw_keyboard():
    # redraws the keyboard
    for letter in letters:
        letter.draw()

while True:
    if GAME_RESULT != "":
        play_again()

    if message_display_time > 0:
        current_time = pygame.time.get_ticks()
        if current_time - message_display_time >= MESSAGE_DISPLAY_DURATION:
            # clear the message
            pygame.draw.rect(SCREEN, "white", (10, 600, 1000, 600))
            # redraw the keyboard
            redraw_keyboard()
            pygame.display.update()
            message_display_time = 0 # reset the message display time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if GAME_RESULT != "":
                    reset()
                else:
                    if len(current_guess_string) == 5 and current_guess_string.lower() in words: # checking for valid guess
                        check_guess(current_guess)
                    else:
                        # display the message and set the display time
                        pygame.draw.rect(SCREEN, "white", (10, 600, 1000, 600))
                        wrong_word_font = pygame.font.Font("assets/FreeSansBold.otf", 40)
                        wrong_word_text = wrong_word_font.render(f"{current_guess_string} is not in the word list.", True, "black")
                        wrong_word_rect = wrong_word_text.get_rect(center = (WIDTH / 2, 700))
                        SCREEN.blit(wrong_word_text, wrong_word_rect)
                        pygame.display.update()
                        message_display_time = pygame.time.get_ticks()
            elif event.key == pygame.K_BACKSPACE:
                if len(current_guess_string) > 0:
                    delete_letter()
            else:
                key_pressed = event.unicode.upper()
                if key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and key_pressed != "":
                    if len(current_guess_string) < 5:
                        create_new_letter(key_pressed)
