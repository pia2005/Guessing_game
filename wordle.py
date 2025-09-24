import random
import csv
word_bank = []

with open('word_bank.csv', 'r', newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        for word in row:
            word_bank.append(word.strip())
word = random.choice(word_bank)

guessedWord = ['_'] * len(word)

attempts = 5
forrige = ""

while True:
    if word == forrige:
        word = random.choice(word_bank)
    else:
        break

while attempts > 0:
    print(f'\n Current word ({len(word)}:' + ' '.join(guessedWord))
    guess = input('Guess a word: ').lower()

    if guess == word:
        print("Gratulerer! du har gjettet riktig ord!")
        break

    found_letter = False
    for letter in guess:
        if letter in word:
            for i in range(len(word)):
                if word[i] == letter:
                    guessedWord[i] = letter
            #print('Great guess!')
            found_letter = True
    # muligens legge inn gule bokstaver

    else:
        attempts -= 1
        print("Wrong guess! Attempts left: " + str(attempts))

    if attempts == 0 and "_" in guessedWord:
        print('\n You\'ve run out of attempts! the word was ' + word)
    
    forrige = word

