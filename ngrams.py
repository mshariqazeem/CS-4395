import pickle
from nltk.util import ngrams
from nltk import word_tokenize


# This function uses the text, provided in the given file,
# to create unigram and bigram dictionaries
def process_file(file):
    # Read file and remove newlines
    f = open(file, 'r', encoding='utf-8')
    raw_text = ''.join(f.read().splitlines())
    f.close()

    # Tokenize the text
    tokens = word_tokenize(raw_text)

    # Create unigrams
    unigrams = tokens

    # Create bigrams
    bigrams = list(ngrams(tokens, 2))

    # Create a dictionary of unigrams and their count
    unigram_dict = {t: unigrams.count(t) for t in set(unigrams)}

    # Create a dictionary of bigrams and their count
    bigram_dict = {b: bigrams.count(b) for b in set(bigrams)}

    # Return both dictionaries
    return unigram_dict, bigram_dict


# Main function
def main():
    # Initialize the file names
    english_file = 'LangId.train.English'
    french_file = 'LangId.train.French'
    italian_file = 'LangId.train.Italian'

    # Get the unigram and bigram dictionaries for all 3 files
    english_unigram_dict, english_bigram_dict = process_file(english_file)
    french_unigram_dict, french_bigram_dict = process_file(french_file)
    italian_unigram_dict, italian_bigram_dict = process_file(italian_file)

    # Save the dictionaries as a pickle file
    pickle.dump(english_unigram_dict, open('english_unigram_dict.p', 'wb'))  # write binary
    pickle.dump(english_bigram_dict, open('english_bigram_dict.p', 'wb'))  # write binary
    pickle.dump(french_unigram_dict, open('french_unigram_dict.p', 'wb'))  # write binary
    pickle.dump(french_bigram_dict, open('french_bigram_dict.p', 'wb'))  # write binary
    pickle.dump(italian_unigram_dict, open('italian_unigram_dict.p', 'wb'))  # write binary
    pickle.dump(italian_bigram_dict, open('italian_bigram_dict.p', 'wb'))  # write binary


# Start here
main()
