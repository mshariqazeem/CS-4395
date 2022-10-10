from urllib import request
from bs4 import BeautifulSoup
import requests
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from collections import defaultdict
import pickle


# This function crawls over a starter URL and finds 15 relevant URLs
def web_crawler(starter_url):
    r = requests.get(starter_url)
    data = r.text
    soup = BeautifulSoup(data, features="html.parser")

    # create a list of URLs
    list_of_urls = []

    # list of urls that should not be used
    wrong_urls = ['https://www.rottentomatoes.com/tv/criminal_minds/s02/reviews',
                  'https://www.metacritic.com/tv/criminal-minds/season-1/critic-reviews',
                  'https://www.bullz-eye.com/television_reviews/2006/criminal_minds_2.htm',
                  'https://www.https://screenrant.com/criminal-minds-season-7-premiere-review/']

    counter = 0
    for link in soup.find_all('a'):
        link_str = str(link.get('href'))
        if ('cbs' not in link_str
            and 'archive' not in link_str
            and 'popmatters' not in link_str
            and 'tvguide' not in link_str) \
                and ('Minds' in link_str or 'minds' in link_str):
            if link_str.startswith('/url?q='):
                link_str = link_str[7:]
            if '&' in link_str:
                i = link_str.find('&')
                link_str = link_str[:i]
            if link_str.startswith('https') \
                    and 'google' not in link_str \
                    and link_str not in wrong_urls \
                    and link_str not in list_of_urls:
                # add URL to the list
                list_of_urls.append(link_str)
                if counter == 14:
                    break
                counter += 1

    return list_of_urls


# This function goes to each of the given urls,
# extracts text from those websites,
# and write the text to a file
def web_scraper(list_of_urls, raw_text_files):
    for i in range(len(list_of_urls)):
        # get a URL
        url = list_of_urls[i]

        html = request.urlopen(url).read().decode('utf8')
        soup = BeautifulSoup(html, features="html.parser")

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out

        # extract text
        text = soup.get_text()

        # open the corresponding file
        f = open(raw_text_files[i], 'w', encoding="utf-8")

        # write text to file
        f.write(text)
        f.close()


# This function reads text from a file,
# removes any extra spaces and new line characters,
# and writes each sentence of the cleaned text to a new file
def text_cleaner(raw_text_files, cleaned_text_files):
    for i in range(len(raw_text_files)):
        # read raw text
        f = open(raw_text_files[i], 'r', encoding="utf-8")
        raw_text = f.read()
        f.close()

        # remove any extra spaces and new line characters
        cleaned_text = ' '.join(raw_text.split())

        # open the new file
        f = open(cleaned_text_files[i], 'w', encoding="utf-8")

        # write each sentence on a new line
        sentences = sent_tokenize(cleaned_text)
        for sentence in sentences:
            f.write(sentence + "\n")

        # close the new file
        f.close()


# takes the list of the cleaned text files
# This function will create tokens from the files
# returns the 40 most popular words in the files
def extract_tokens(cleaned_text_files):
    text = ""
    for i in range(len(cleaned_text_files)):
        # read raw text
        f = open(cleaned_text_files[i], 'r', encoding="utf-8")
        text += f.read()
        f.close()
    # Create sentences of files
    sentences = sent_tokenize(text)
    # Create tokens for file and clean it up
    words = word_tokenize(text)
    words = [w.lower() for w in words if w.lower() not in stopwords.words('english') and (w.isalpha() or w.isnumeric())]
    # get a frequency list of files
    frequency = dict(Counter(words))
    frequency = dict(reversed(sorted(frequency.items(), key=lambda item: item[1])))

    # Gets the most frequent words in the files
    words = []
    for i in frequency:
        if len(words) == 40:
            break
        words.append(i)

    return sentences, words


# This function takes the words you want to make a knowledge base
# look for the words in the relevant sentences
# returns the knowledge base for chat bot
def searchable_knowledgebase(words, sentences):
    knowledge_base = defaultdict(str)
    for sentence in sentences:
        for word in words:
            # if the word is in the sentence add to knowledge base
            if word in sentence.lower():
                knowledge_base[word] += " " + sentence
    return knowledge_base


# Main function
def main():
    # initialize a starter url
    starter_url = "https://en.wikipedia.org/wiki/Criminal_Minds"

    # get a list of relevant urls, within the starter url
    list_of_urls = web_crawler(starter_url)
    print("Found 15 Relevant websites from the starter URL.")

    # create a list of files
    raw_text_files = []
    cleaned_text_files = []

    # generate file names
    for i in range(len(list_of_urls)):
        raw_text_files.append("rawText" + str(i + 1) + ".txt")
        cleaned_text_files.append("cleanedText" + str(i + 1) + ".txt")

    # extract text from urls and write it to files
    web_scraper(list_of_urls, raw_text_files)
    print("Scraped text from all the found websites.")

    # clean up the text and write it to new files
    text_cleaner(raw_text_files, cleaned_text_files)
    print("Cleaned up the text scraped from all the found websites.")

    # extracts tokens and get the most popular words that aren't stop words
    sentences, words = extract_tokens(cleaned_text_files)
    print("Top 40 words on websites " + str(words))

    # top 10 words for chat bot
    knowledge_base = ["criminal", "minds", "series", "fbi", "episode", "season", "new", "tv", "review", "deadline"]
    # create a dict of a searchable knowledge base
    knowledge = searchable_knowledgebase(knowledge_base, sentences)

    pickle.dump(knowledge, open('knowledge_base.p', 'wb'))  # write binary


# The program starts here
main()
