import sys
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import random
import nltk


# Preprocess the given raw text
def process_text(raw_text):
    # Get tokens that are alpha, not in the NLTK stopwords list, and have length > 5
    big_words = [t.lower() for t in word_tokenize(raw_text)
                 if t.isalpha()
                 and t not in stopwords.words('english')
                 and len(t) > 5]

    # Lemmatize the words
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in big_words]

    # Get the unique lemmas
    lemmas_set = set(lemmas)

    # Pos tag the unique lemmas and print the first 20 tagged lemmas
    tags = nltk.pos_tag(lemmas_set)
    print("\nThe first 20 tagged unique lemmas:\n", tags[:20])

    # Create a list of lemmas that are nouns
    nouns = []
    for token, pos in tags:
        if pos[0] == 'N':
            nouns += [token]

    print("\nThe number of tokens that are alpha, not in the NLTK stopword list, and have length > 5: ", len(big_words))
    print("The number of nouns: ", len(nouns))

    return big_words, nouns


# Print letters in the given list, with a space between them
def print_word(guessed_word):
    for w in guessed_word:
        print(w, end=' ')


# Compare the guessed word with the selected word
def compare_words(guessed_word, selected_word):
    for i in range(len(guessed_word)):
        if guessed_word[i] != selected_word[i]:
            return False
    return True


# Create a guessing game using the given list of words
def guessing_game(words):
    points = 5
    game_over = False

    # Print the instructions for the game
    print("\nGuessing Game Started!"
          "\nInitially, You have 5 points."
          "\nEach correct guess will increase your points."
          "\nEach wrong guess will decrease your points."
          "\nDuplicate guesses does not increase or decrease your points."
          "\nGame will end if your points reaches -1."
          "\nTo end the game, Enter '!'.")

    # Play as long as the game is not over
    while not game_over:
        # Select a random word
        selected_word = random.choice(words)

        # Create a word filled with underscores '_'
        blanked_word = []
        for i in range(len(selected_word)):
            blanked_word.append("_")
        print("\nYour word is:", end=' ')
        print_word(blanked_word)

        # Stores all the guessed letters for each word
        guesses = []

        while not game_over:
            # Ask the user for input
            user_guess = input("\nGuess a letter : ")[0].lower()
            # If the user entered '!', end the game
            if user_guess[0] == '!':
                game_over = True
                print("Game Over! You ended the game.")
                break
            # Check if user's guessed letter is in the word
            else:
                # If the user has already guessed this letter, ask them to try again
                if user_guess in guesses:
                    print("Already Guessed! Try Again. You still have", points, "points.")
                # Check if the newly guessed letter is in the word
                else:
                    guess_found = False
                    # Go through the selected word to see if any of the letters match the user's guess
                    for k in range(len(selected_word)):
                        # If any of the letters match the user's guess, fill in the matched word
                        if user_guess == selected_word[k]:
                            guess_found = True
                            blanked_word[k] = selected_word[k]
                    # If the letter was found, increase the points
                    if guess_found:
                        points += 1
                        # If the entire word has been guessed, go to the next word
                        if compare_words(blanked_word, selected_word):
                            print("Good Job! You solved it.")
                            print_word(selected_word)
                            print("\nYou have", points, "points.")
                            break
                        # If the entire word has not been guessed, add the user's guess to the list of guesses
                        else:
                            guesses += [user_guess]
                            print("Right! You have", points, "points.")
                    # If the letter was not found, decrease the points
                    else:
                        points -= 1
                        # If the points have reached -1, end the game
                        if points < 0:
                            game_over = True
                            print("Game Over! You ran out of points."
                                  "\nThe word was:", selected_word)
                            break
                        # If the points >= 0, add the user's guess to the list of guesses
                        else:
                            guesses += [user_guess]
                            print("Sorry!! Try Again. You have", points, "points.")
                # Print the word, with all the guessed letters filled
                print("The word so far:", end=' ')
                print_word(blanked_word)


# Main function
def main():
    # Check if the file path has been specified in the sys.arg
    if len(sys.argv) <= 1:
        print('Error: File path not specified')
    else:
        # Open file for reading
        input_file = open(str(sys.argv[1]), 'r')
        # Read the entire file in the variable 'raw_text'
        raw_text = input_file.read()
        # Close the file
        input_file.close()

        # Word_tokenize the raw_text and get the unique tokens
        tokens = [t.lower() for t in word_tokenize(raw_text)]
        tokens_set = set(tokens)

        # Print the lexical diversity of the document
        print("Lexical diversity: %.2f" % (len(tokens_set) / len(tokens)))

        # Get all the big tokens and nouns from the raw_text
        big_words, nouns = process_text(raw_text)

        # Create a dictionary of all the nouns and their count
        nouns_dict = {}
        for noun in nouns:
            nouns_dict[noun] = big_words.count(noun)

        # Stores 50 most common nouns
        common_nouns = []
        # Print the 50 most common nouns and their count
        print("\nThe 50 most common words and their counts:")
        for noun in sorted(nouns_dict, key=nouns_dict.get, reverse=True)[:50]:
            print(noun, ':', nouns_dict[noun])
            common_nouns += [noun]

        # Start the guessing game
        guessing_game(common_nouns)


# Start here
main()
