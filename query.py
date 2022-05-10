from importlib.util import set_loader
from operator import contains
from parso import parse
import file_io as io
import re
import sys
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


class query():

    STOP_WORDS = set(stopwords.words('english'))
    token_regex = r"\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+"
    stemmer = PorterStemmer()

    def __init__(self, bool, titles, docs, words, type_in):
        """
        :param bool: True or False, this allows our query to know whether to output the
        top ten pages whilst taking pagerank into account or without pagerank.
        :param titles: this is the title file containing our id_to_titles dictionary 
        compiled from the indexer.
        :param docs: this is the docs file containing our pagerank_prime dictionary 
        compiled from the indexer.
        :param words: this is the words file containing our word_to_rel dictionary 
        compiled from the indexer.
        :param type_in: this is the input the user is searching upon.

        These are all the dictionaries we will be using throughout the query class.
        Below the dictionaires there are also a few global variable to be used in index.

        This function gets called whenever the query class get initialised. So inside 
        are all the function calls required to output the print statements to display
        the top ten (if possible) results.
        """
        self.quer_id_to_titles = {}
        self.quer_pagerank = {}
        self.quer_word_to_rel = {}
        self.word_sum = {}
        self.page_values = {}

        io.read_title_file(titles, self.quer_id_to_titles)
        io.read_docs_file(docs, self.quer_pagerank)
        io.read_words_file(words, self.quer_word_to_rel)

        self.ifpagerank(bool, type_in)

    def ifpagerank(self, bool, type_in):
        """
        This function controls whether our score will include pagerank or not.

        :param bool: this is the bool from our command line controlling the pagerank decision.
        :param type_in: this is the user input that get passed along to parse.
        :return: the top ten (if possible) results (the output of the respective score function).
        """
        if bool:
            return self.pagerank_score(self.parse(type_in))
        else:
            return self.score(self.parse(type_in))

    def parse(self, all_words):
        """
        This function parses our user input.

        :param all_words: this is the user input that get passed along to parse.
        :return: the parsed string of words.
        """
        parse_word_token = re.findall(self.token_regex, all_words)
        word_string = []
        for word in parse_word_token:
            word: str = word.lower()
            if word not in self.STOP_WORDS:
                word = self.stemmer.stem(word)
                word_string.append(word)
        return word_string

    def score(self, searched_words):
        """
        This function controls the score when pagerank is not included.

        :param searched_words: this is the user input that has been parsed.
        :return: the top ten (if possible) results.
        """
        for pageid in self.quer_id_to_titles:
            word_sum = 0
            for word in searched_words:
                if pageid in self.quer_word_to_rel[word]:
                    word_sum += self.quer_word_to_rel[word][pageid]
            self.page_values[pageid] = word_sum
        self.page_values = dict((self.quer_id_to_titles[key], value) for (
            key, value) in self.page_values.items())
        count = 1
        for (key, value) in sorted(self.page_values.items(), key=lambda x: x[1], reverse=True):
            if count <= 10:
                print(key)
                count += 1

    def pagerank_score(self, searched_words):
        """
        This function controls the score when pagerank is included.

        :param searched_words: this is the user input that has been parsed.
        :return: the top ten (if possible) results.
        """
        for pageid in self.quer_id_to_titles:
            word_sum = 0
            for word in searched_words:
                if pageid in self.quer_word_to_rel[word]:
                    word_sum += self.quer_word_to_rel[word][pageid]
            word_sum = word_sum ** (1/2)
            self.page_values[pageid] = word_sum * self.quer_pagerank[pageid]
        self.page_values = dict((self.quer_id_to_titles[key], value) for (
            key, value) in self.page_values.items())
        count = 1
        for (key, value) in sorted(self.page_values.items(), key=lambda x: x[1], reverse=True):
            if count <= 10:
                print(key)
                count += 1


if __name__ == "__main__":
    """
    This function controls the repl.

    :return: this passes the typed input to the query class. The repl will
    break if the keyword "quit" is typed in.
    """
    try:
        if len(sys.argv) - 1 == 4 and sys.argv[1] == "--pagerank":
            titles = sys.argv[2]
            docs = sys.argv[3]
            words = sys.argv[4]
            while True:
                type_in = input(">> ")
                if type_in == ":quit":
                    break
                runquery = query(True, titles, docs, words, type_in)

        elif len(sys.argv) - 1 == 3:
            titles = sys.argv[1]
            docs = sys.argv[2]
            words = sys.argv[3]
            while True:
                type_in = input(">> ")
                if type_in == ":quit":
                    break
                runquery = query(False, titles, docs, words, type_in)

        else:
            raise AttributeError("Invalid inputs.")

    except(IOError, FileNotFoundError):
        print("Input error.")
        sys.exit
