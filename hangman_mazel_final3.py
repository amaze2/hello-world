#hangman
#Adam Mazel
#LIS 485: Intro to Programming

import random

#hangman tuple as global constant
HANGMANPICS = ('''
 +---+
 |
 |
 |
 |
 |
=========''', '''
 +---+
 | |
 |
 |
 |
 |
=========''', '''
 +---+
 | |
 O |
 |
 |
 |
=========''', '''
 +---+
 | |
 O |
 | |
 |
 |
=========''', '''
 +---+
 | |
 O |
 /| |
 |
 |
=========''', '''
 +---+
 | |
 O |
 /|\ |
 |
 |
=========''', '''
 +---+
 | |
 O |
 /|\ |
 / |
 |
=========''', '''
 +---+
 | |
 O |
 /|\ |
 / \ |
 |
=========''', '''
 +---+
 | |
 O |
 /|\ |
 / \ |
 | | 
=========''')

#print hangman-in-progress function
def hangman(incorrectLetters, guess, wrongGuesses):
	print("Incorrect! Sorry!")
	incorrectLetters.append(guess)
	wrongGuesses += 1
	print(HANGMANPICS[-1 + wrongGuesses])
	print("You have ", (len(HANGMANPICS) - wrongGuesses), "wrong guesses remaining.")

#print incorrect guesses function
def incorrectGuesses(wrongGuesses, incorrectLetters):
	if wrongGuesses != 0:
		print("Incorrect guesses:", incorrectLetters)

#main function
def main():
	#control loop with variable
	play = "y"

	#initialize and set accumulators
	gamesPlayed = 0
	gamesWon = 0
	wrongGuesses = 0
	
	#create empty lists to hold correct and incorrect letters
	correctLetters = []
	incorrectLetters = []

	#play loop
	while play == "y":	
		#randomly create secret word from tuple of 10 words
		word = random.choice(("archive", "library", "python", "code", "information", "computer", "technology", "program", "digital", "museum"))
		
		#accumulate number of games played for statistical purposes
		gamesPlayed += 1
		
		#second play loop (display hidden word, letters in word, etc.)
		while wrongGuesses < len(HANGMANPICS):
			hiddenWord = ""
			for letter in word:
				if letter in correctLetters:
					hiddenWord += letter
				else:
					hiddenWord += "_"
			if hiddenWord == word:
				print("Congratulations! You win! You guessed:", word)
				gamesWon += 1
				break
		
			#query user for guess, validate input for capitalization
			print("Please guess a letter in the following word:", hiddenWord)
			guess = input().lower()
		
			#validate user input (alpha character)
			if not guess.isalpha():
				print("Your guess must be a letter, not a number, symbol, etc. Guess again: ")
		
			#validate user input (character length)
			if len(guess) != 1:
				print("Your guess must be one character long. Guess again:" )
		
			#keep track of guesses and if user duplicates a guess, make user guess again
			if guess in correctLetters or guess in incorrectLetters:
				print("You have already guessed ", guess, ". Guess again: ")
			
			#correct guess and keep track of correct guesses
			elif guess in word:
				print("Correct! Good job!")
				correctLetters.append(guess)
			
			#hangman function
			else:
				hangman(incorrectLetters, guess, wrongGuesses)
				wrongGuesses +=1
			
			#incorrect guesses function	
			incorrectGuesses(wrongGuesses, incorrectLetters)
			
			print()
	
		#run out of guesses
		if wrongGuesses == len(HANGMANPICS):
			print("You died by hanging because you ran out of guesses. You failed to guess:", word)
		
		#allow user to play multiple games
		print("Do you want to play again? y / n: ")
		play = input().lower()
		if play == "y":
			wrongGuesses = 0
			correctLetters = []
			incorrectLetters = []
		
		#stop play and print player performance stats
		else:
			print("You won ", gamesWon, "games out of", gamesPlayed, " games played.")
			
main()