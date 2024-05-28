# Program Name: Number Guessing Game
# Author: Gordon La
# Description: This program is a number guessing game where the player must guess a random number within a given range,
# based on the selected difficulty level. The game records high scores and allows multiple rounds.

import random

# Program's main function
def main():
    # Constants for the difficulty levels
    EASY, MEDIUM, HARD = 100, 1000, 10000
    HIGH_SCORE_FILE = 'high_score.txt'

    playing = True  # Flag to control the game loop

    while playing:
        print("**************************************************")
        print("      ⭐      GORDON'S GUESSING GAME︎      ⭐")
        print('**************************************************')
        print(f'\n{"1. Play Game":>29}\n{"2. How To Play":>31}\n{"3. High Scores":>31}\n{"4. Quit":>24}')

        playing = menu_choice(EASY, MEDIUM, HARD, HIGH_SCORE_FILE)  # Call the menu function to determine the next action

# Function to display the menu and handle the user's choice
def menu_choice(EASY, MEDIUM, HARD, HIGH_SCORE_FILE):
    while True:
        try:
            choice = int(input("\nSelect a number from the menu to proceed: "))  # User's choice from the menu

            if 1 <= choice <= 4:
                if choice == 1:
                    play_game(EASY, MEDIUM, HARD, HIGH_SCORE_FILE)
                    print("")
                    return True
                elif choice == 2:
                    how_to_play()
                elif choice == 3:
                    high_scores(HIGH_SCORE_FILE)
                else:
                    print("\nThanks for playing my game! 👋")
                    return False
            else:
                print("Invalid input. Must be a whole number from 1 to 4.")
                
        except ValueError:
            print("Invalid input. Must be a whole number from 1 to 4.")

# Function for performing the best guess implementation
def play_game(EASY, MEDIUM, HARD, HIGH_SCORE_FILE):
    play_again = True  # Flag to control the play again loop

    while play_again:
        print("\n***********\n PLAY GAME \n***********")
        name = input("\nEnter your name: ")  # Player's name input
        print("\n1. Easy\n2. Medium\n3. Hard")

        select_difficulty = True  # Flag to control the difficulty selection loop
        while select_difficulty:
            try:
                difficulty = int(input("\nSelect a difficulty: "))  # Difficulty choice

                if 1 <= difficulty <= 3:
                    select_difficulty = False
                else:
                    print("Invalid input. Must be a whole number from 1 to 3.")
            except ValueError:
                print("Invalid input. Must be a whole number from 1 to 3.")
        
        min_score = find_high_score(HIGH_SCORE_FILE)  # Retrieve the lowest score from file

        if min_score == -1:
            print("\nI didn't find a high score file, so let's see how well you can do!")

        if difficulty == 1:
            max_num = random.randint(50, EASY)  # Set the maximum number for Easy level
        elif difficulty == 2:
            max_num = random.randint(EASY + 1, MEDIUM)  # Set the maximum number for Medium level
        elif difficulty == 3:
            max_num = random.randint(MEDIUM + 1, HARD)  # Set the maximum number for Hard level

        num = random.randint(1, max_num)  # Random number to be guessed

        print(f"\nI'm thinking of a number from 1 to {max_num}.")

        guess_list = []  # List to store the guesses
        counter = 0  # Counts the number of attempts

        guessing = True  # Flag that controls the guessing loop
        
        while guessing:
            try:
                guess = int(input("\nWhat is your guess? "))  # Player's guess

                if guess == num:
                    counter += 1

                    print(f"\n🎯 You guessed it! 🎯")

                    if counter == 1:
                        print(f"It took you only 1 try to get it. Nice!")
                    else:
                        print(f"It took you {counter} tries to get it.")

                    guess_list.append(guess)  # Add the guess to the list
                    print("Your guesses:", end=' ')
                    prev_guesses(guess_list)  # Display previous guesses

                    if counter < min_score or min_score == -1:
                        print("\n********************************************")
                        print("      🏆      CONGRATULATIONS!      🏆")
                        print("********************************************")
                        print("        You have a new record best!!")
                        
                    if counter > min_score and min_score != -1:
                        print(f"\nGood try. But the best score is still {min_score}.")
                    
                    file = open(HIGH_SCORE_FILE, 'a')  # Open the high score file in append mode
                    file.write(f"{counter} {name}\n")  # Write the new score and name
                    file.close()

                    answering = True  # Flag that controls the play again question loop

                    while answering:
                        try:
                            answer = input("\nWould you like to play again? (Y / N): ")  # Play again choice

                            if answer == "Y" or answer == "y":
                                answering, guessing = False, False
                            elif answer == "N" or answer == "n":
                                answering, guessing, play_again = False, False, False
                            else:
                                print("Invalid input. Enter 'Y' for yes or 'N' for no.")
                    
                        except ValueError:
                            print("Invalid input. Enter 'Y' for yes or 'N' for no.")

                else:
                    wrong_guess(num, guess)  # Handle incorrect guesses

                    if guess_list:
                        print("Your previous guesses:", end=' ')
                        prev_guesses(guess_list)  # Display previous guesses
                        
                    guess_list.append(guess)
                    counter += 1
            except ValueError:
                print("Invalid input. Must be a whole number.")

# Function to display the instructions for the game.
def how_to_play():
    print("\n*************\n HOW TO PLAY \n*************")
    print("\nWelcome to Gordon's Number Guessing Game! 🤩")
    print("\nIn this game, I will think of a number from 1 to a random maximum number based on the selected difficulty.")
    print("Your mission, should you choose to accept it, will be to guess the number I'm thinking of.")

# Function to display the high scores
def high_scores(HIGH_SCORE_FILE):
    try:
        data = score_list(HIGH_SCORE_FILE)  # Get the list of high scores
        print("\n*************\n HIGH SCORES \n*************")
        
        print(f"\n{'Name':<20}{'Score'}\n{'----':<20}{'-----'}")

        if len(data) > 5:
            for i in range(5):
                score, name = data[i]
                print(f"{name:<20}{score}")
        else:
            for score, name in data:
                print(f"{name:<20}{score}")

    # See more about FileNotFoundError here: https://docs.python.org/3/library/exceptions.html#FileNotFoundError           
    except FileNotFoundError:
        print("Sorry, I couldn't find a file containing high scores. 😕")

# Function to read scores from a file and return a sorted list of tuples (score, name)
def score_list(HIGH_SCORE_FILE):
    file = open(HIGH_SCORE_FILE, 'r')
    lines = file.readlines()
    file.close()

    data = []
    for line in lines:
        score, name = line.strip().split()
        data.append((int(score), name))
    data.sort()  # Sort the list of tuples from lowest to highest score
    return data

# Function to find the highest score in the high score list
def find_high_score(HIGH_SCORE_FILE):
    try:
        data = score_list(HIGH_SCORE_FILE)  # Get the list of scores
        return data[0][0]  # Return the lowest score (at the top of the list)
    except FileNotFoundError:
        return -1  # Return -1 if the file is not found

# Function to provide feedback if the guess is too low or too hig
def wrong_guess(num, guess):
    if guess < num:
        print(f"\n▼▼ TOO LOW ▼▼ Guess higher than {guess}.")
    else:
        print(f"\n▲▲ TOO HIGH ▲▲. Guess lower than {guess}.")

# Function to print previous guesses
def prev_guesses(guess_list):
    for i in range(len(guess_list)):
        if i < len(guess_list) - 1:
            print(guess_list[i], end=', ')
        else:
            print(guess_list[i])

if __name__ == "__main__":
    main()
