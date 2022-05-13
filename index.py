import re
import sys
import xml.etree.ElementTree as et
from math import log

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

import file_io as io

# thisvar = Indexer('/Users/maximbeekenkamp/Desktop/Computer Science/CSCI 200/projects/Search Engine/PageRankExample1.xml', 'titles.xml', 'docs.xml', 'words.xml')


class Indexer:
    """
    This class contains all the indexing functionality for the programme.
    """

    def __init__(self, wiki, titles, docs, words):
        """
        :param wiki: this is the wiki xml file that this program will index.
        :param titles: this is the title file that our id_to_titles dictionary 
        will write to for our query.
        :param docs: this is the docs file that our pagerank_prime dictionary 
        will write to for our query.
        :param words: this is the words file that our word_to_rel dictionary 
        will write to for our query.

        These are all the dictionaries we will be using throughout the indexer class.
        Below the dictionaires there are also a few global variable to be used in index.

        This function gets called whenever the Indexer class get initialised. So inside 
        are all the function calls required to output the finalised dictionaires we will
        be using in query.
        """

        self.titles_to_ids = {}
        self.ids_to_titles = {}
        self.links = {}
        self.weights = {}
        self.pagerank = {}
        self.pagerank_prime = {}
        self.id_to_max = {}
        self.word_to_rel = {}
        self.word_to_page = {}
        self.stemmer = PorterStemmer()
        self.n = 0
        self.STOP_WORDS = set(stopwords.words('english'))
        self.token_regex = r"\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+"

        self.parser(wiki)
        io.write_docs_file(docs, self.pagerank_prime)
        io.write_title_file(titles, self.ids_to_titles)
        io.write_words_file(words, self.word_to_rel)

    def parser(self, wiki):
        """
        The function parser will parse our input xml file.

        :param: wiki, this is the xml file which needs to be parsed.
        :return: self - the updated dictionaries
        """
        wiki_tree = et.parse(wiki)
        wiki_root = wiki_tree.getroot()

        for wiki_page in wiki_root.findall("page"):
            page_id: int = int(wiki_page.find("id").text)
            page_title: str = str(wiki_page.find("title").text.strip())
            page_title = self.stemmer.stem(page_title)
            page_title = page_title.lower()
            self.links[page_id] = []
            self.titles_to_ids[page_title] = page_id
            self.ids_to_titles[page_id] = page_title

            wiki_text = wiki_page.find("text").text
            wiki_page_token = re.findall(
                self.token_regex, wiki_text + " " + page_title)
            for word in wiki_page_token:
                word: str = word.lower()
                if word not in self.STOP_WORDS:
                    word = self.stemmer.stem(word)

                    if self.isLink(word):
                        linktitle, linktext = self.sep_link(word)
                        if linktext != "":
                            for linkword in linktext:
                                linkword = linkword.lower()
                                if linkword not in self.STOP_WORDS:
                                    linkword = self.stemmer.stem(linkword)
                                    self.addfreq(linkword, page_id)
                        self.links[page_id].append(linktitle)
                    else:
                        self.addfreq(word, page_id)
            self.tf(page_id)
        self.n = len(set(self.titles_to_ids))
        self.update_tf()
        self.pageranking()

    def isLink(self, word: str):
        """
        This will check if our input string is a link or not.
        output will look like:
        True
        False

        :param word: is a string which is the string we're checking
        :return: bool, true or false.
        """
        return (word[0] == "[")

    def sep_link(self, word: str) -> tuple[str, str]:
        """
        This will seperate links when they have the | character seperating 
        the linked word(s) with the title of the page they're linking to.
        output will look like:
        tuple(linktitle, linktext)

        :param word: is a string which is the string we're checking.
        :return: a tuple of the link title and the link text.
        """
        var = word[2: -2]

        if "|" in var:
            # edge case of nothing before/after verticle bar
            link_words = var.split("|")
            linktitle = link_words[0].strip()
            linktitle = linktitle.lower()
            linktitle = self.stemmer.stem(linktitle)
            linktext = link_words[1]  # [[Greek|]]
            linktext = re.findall(self.token_regex, linktext)
            return linktitle, linktext
        else:
            linktitle = var.strip()
            linktitle = linktitle.lower()
            linktitle = self.stemmer.stem(linktitle)
            linktext = var
            linktext = re.findall(self.token_regex, linktext)
            return linktitle, linktext

    def addfreq(self, word: str, pageid: int):
        """
        This will update the frequency of a word in a page as we go along to
        prevent from looping through our xml file excessively. This also 
        handles all unique word portions of search, which are only required
        within the tfidf portion of search.

        :param word: the string word we're using as a key in the dictionaries
        :param pageid: the int pageid we're using as a key in the dictionaries
        :return: the dictionary word to page to frequency updated and the 
        dictionary id to max updated.
        """
        if word not in self.word_to_rel:
            self.word_to_rel[word] = {}
        if pageid not in self.word_to_rel[word]:
            self.word_to_rel[word][pageid] = 1
        else:
            self.word_to_rel[word][pageid] += 1
        if pageid not in self.id_to_max:
            self.id_to_max[pageid] = 1
        else:
            self.id_to_max[pageid] = max(
                self.id_to_max[pageid], self.word_to_rel[word][pageid])
        if word not in self.word_to_page:
            self.word_to_page[word] = [pageid]
        if pageid not in self.word_to_page[word]:
            self.word_to_page[word].append(pageid)

    def tf(self, pageid: int):
        """
        This will update the word to pageid to frequency dictionary to a word to
        pageid to term frequency dictionary. 

        :param word: the string word we're using as a key in the dictionary
        :param pageid: the int pageid we're using as a key in the dictionary
        :return: the dictionary word to page to term frequency.
        """
        for word in self.word_to_rel:
            if pageid in self.word_to_rel[word]:
                self.word_to_rel[word][pageid] = self.word_to_rel[word][pageid] \
                    / self.id_to_max[pageid]

    def idf(self, word: str):
        """
        This will update the word to page dictionary to a word to
        idf dictionary. 

        :param word: the string word we're using as a key in the dictionary
        :return: the dictionary word to idf.
        """
        self.word_to_page.update(
            {word: log(self.n/len(set(self.word_to_page[word])))})

    def relevance(self, word: str, pageid: int):
        """
        This will update the word to pageid to  term frequency dictionary to a word to
        pageid to relevance dictionary. 

        :param word: the string word we're using as a key in the dictionary
        :param pageid: the int pageid we're using as a key in the dictionary
        :return: the dictionary word to pageid to relevance.
        """
        self.word_to_rel[word][pageid] = self.word_to_rel[word][pageid] * \
            self.word_to_page[word]

    def update_tf(self):
        """
        This combines the previous three functions allowing us to call just it
        instead of all three functions. 

        :return: the dictionary word to pageid to relevance.
        """
        for word in self.word_to_rel:
            self.idf(word)
            for pageid in self.word_to_rel[word]:
                self.relevance(word, pageid)

    def trimming(self):
        """
        This removes all duplicates, links to outside the corpus, and links to themselves. 

        :return: the dictionary pageid to link titles.
        """
        for pageid in self.links:
            self.links[pageid] = set([title for title in self.links[pageid]
                                      if title in self.titles_to_ids and
                                      not(title == self.ids_to_titles[pageid])])

    def weight(self):
        """
        This will precalculate the weights for every page. This also calls trimming so
        that it receives the most uptodate dictionaries.

        :return: the dictionary word to title to weight.
        """
        self.trimming()
        e = 0.15
        for pageid in self.links:
            self.weights[pageid] = {}
            nk = len(self.links[pageid])
            if nk == 0:
                for title in self.titles_to_ids:
                    if not title == self.ids_to_titles[pageid]:
                        self.links[pageid].add(title)
            for title in self.titles_to_ids:
                if title in self.links[pageid]:
                    nk = len(self.links[pageid])
                    self.weights[pageid][title] = (e/self.n) + ((1-e)/nk)
                else:
                    self.weights[pageid][title] = e/self.n

    def distance(self) -> float:
        """
        This will calculate the euclidean distance for rank. 

        :return: float value of the euclidean distance for rank.
        """
        var = 0
        for pageids in self.ids_to_titles:
            var += (self.pagerank_prime[pageids] - self.pagerank[pageids])**2
        return ((var)**(1/2))

    def pageranking(self):
        """
        This will calculate the final pagerank after convergence. 

        :return: the pageid to pagerank dictionary at convergence.
        """
        self.weight()
        for pageids in self.ids_to_titles:
            self.pagerank[pageids] = 0
            self.pagerank_prime[pageids] = 1/self.n
        delta = 0.001
        while self.distance() > delta:
            self.pagerank = self.pagerank_prime.copy()
            for pageid_j in self.ids_to_titles:
                self.pagerank_prime[pageid_j] = 0
                title_j = self.ids_to_titles[pageid_j]
                for pageid_k in self.ids_to_titles:
                    self.pagerank_prime[pageid_j] += \
                        self.weights[pageid_k][title_j] * \
                        self.pagerank[pageid_k]


if __name__ == "__main__":
    """
    argv[0]:
    This is path of the python file index.py
    argv[1]:
    This is the wiki file path, is the name of the input file that the indexer will read in and 
    parse.
    argv[2]: 
    This is the titles file path, which maps document IDs to document titles.
    argv[3]:
    This is the docs filepath, which stores the rankings computed by PageRank.
    argv[4]:
    This is the words filepath, which stores the relevance of documents to words.
    """
    try:
        if len(sys.argv) - 1 != 4:
            raise AttributeError(
                "Invalid number of inputs. There must be exactly four inputs.")
        wiki = sys.argv[1]
        titles = sys.argv[2]
        docs = sys.argv[3]
        words = sys.argv[4]

        Indexer(wiki, titles, docs, words)

    except(IOError, FileNotFoundError):
        print("Input error.")
        sys.exit
