import pickle
from nltk.util import ngrams
from nltk import word_tokenize


def main():

    # store text into a list
    text = []
    with open('LangId.test', 'r', encoding='utf-8') as f:
        for line in f:
            text.extend([line[:-1]])

    languages_used = ['English', 'French', 'Italian']

    laplace(text, languages_used)

    # store correct languages into a list
    language = []
    with open('LangId.sol', 'r', encoding='utf-8') as f:
        for line in f:
            language.append(line.split()[-1])
    # store guesses into a list
    guesses = []
    with open('guesses.txt', 'r', encoding='utf-8') as f:
        for line in f:
            guesses.append(line.split()[-1])

    # compares guesses with the actual language
    accurate, mismatch = accuracy(guesses, language)
    print("Accuracy: " + str(int(accurate*100)) + "%")
    print("Lines wrongly classified: " + str(mismatch))


# load_Languages will store the languages used into a dictionary
# returns the total vocabulary and dict of languages
def load_languages(languages_used):
    vocabulary = 0
    # store the languages into a dictionary
    languages = {}
    # loops through the languages usd
    for language in languages_used:
        unigram = pickle.load(open(language.lower()+'_unigram_dict.p', 'rb'))
        bigram = pickle.load(open(language.lower()+'_bigram_dict.p', 'rb'))
        languages[language] = (bigram, unigram)
        # Adding to the total vocabulary for laplace algorithm
        vocabulary += len(unigram)

    return languages, vocabulary


# laplace will use the laplace algorithm to guess the language
# returns a list of the predictions for the languages
def laplace(text, languages_used):

    languages, vocabulary = load_languages(languages_used)

    f = open("guesses.txt", "w")

    for line in range(len(text)):
        unigrams = word_tokenize(text[line])  # unigrams of current line
        bigrams = list(ngrams(unigrams, 2))  # bigrams of the unigrams

        max_prob = 0  # placeholder max value
        guess = 'English'  # placeholder guess
        # loops through each language
        for language in languages:
            cur_prob = 1
            # loops through each bigram
            for bigram in bigrams:

                n = languages[language][0][bigram] if bigram in languages[language][0] else 0
                d = languages[language][1][bigram[0]] if bigram[0] in languages[language][1] else 0
                # laplace algorithm equation
                cur_prob *= (n + 1) / (d + vocabulary)

            # check if guess needs to be changed
            if cur_prob > max_prob:
                max_prob = cur_prob
                guess = language
        f.write(str(line+1)+" "+guess+"\n")
    f.close()


# accuracy will calculate how accurate is the guess compared to the actual
# returns accuracy and the wrongly predicted lines
def accuracy(guess, correct):
    wrong_lines = []  # stores wrong lines
    inaccurate = 0  # stores how many inaccurate
    # loops to see if the values are the same or not
    for index in range(len(guess)):
        if guess[index] != correct[index]:
            inaccurate += 1
            wrong_lines.append(index+1)
    return 1 - inaccurate/len(guess), wrong_lines


if __name__ == "__main__":
    main()
