import index
import query
import pytest

#this tests the functions within tf idf
def test_tf_idf():
    index_test = index.Indexer("SearchDesignCheck.xml",'titles.xml', 'docs.xml', 'words.xml').word_to_rel
    assert index_test == {'librari': {1: 0.4054651081081644, 2: 0.13515503603605478}, 'contain': {1: 0.5493061443340549}, 'book': {1: 0.2027325540540822, 3: 0.13515503603605478}, 'histori': {1: 0.2027325540540822, 2: 0.4054651081081644}, 'brown': {1: 0.4054651081081644, 3: 0.13515503603605478}, 'univers': {1: 0.0, 2: 0.0, 3: 0.0}, 'old': {1: 0.2027325540540822, 3: 0.13515503603605478}, 'rhode': {1: 0.5493061443340549}, 'island': {1: 0.5493061443340549}, 'studi': {2: 0.27031007207210955, 3: 0.13515503603605478}, 'document': {2: 0.3662040962227032}, 'past': {2: 0.3662040962227032}, 'peopl': {2: 0.13515503603605478, 3: 0.13515503603605478}, 'institut': {3: 0.3662040962227032}, 'higher': {3: 0.3662040962227032}, 'educ': {3: 0.3662040962227032}, 'research': {3: 0.3662040962227032}, 'oxford': {3: 0.3662040962227032}, 'older': {3: 0.3662040962227032}, 'univ': {3: 0.3662040962227032}}
    index_test1 = index.Indexer("SearchDesignCheck.xml",'titles.xml', 'docs.xml', 'words.xml').word_to_page
    assert index_test1 == {'librari': 0.4054651081081644, 'contain': 1.0986122886681098, 'book': 0.4054651081081644, 'histori': 0.4054651081081644, 'brown': 0.4054651081081644, 'univers': 0.0, 'old': 0.4054651081081644, 'rhode': 1.0986122886681098, 'island': 1.0986122886681098, 'studi': 0.4054651081081644, 'document': 1.0986122886681098, 'past': 1.0986122886681098, 'peopl': 0.4054651081081644, 'institut': 1.0986122886681098, 'higher': 1.0986122886681098, 'educ': 1.0986122886681098, 'research': 1.0986122886681098, 'oxford': 1.0986122886681098, 'older': 1.0986122886681098, 'univ': 1.0986122886681098}

#this tests the components of pagerank
def test_components_of_pagerank():
    index_test = index.Indexer("SearchDesignCheck.xml",'titles.xml', 'docs.xml', 'words.xml').trimming()
    assert index_test == {1: {'histori', 'univers'}, 2: {'univers', 'libraries at brown'}, 3: set()}
    index_test1 = index.Indexer("SearchDesignCheck.xml",'titles.xml', 'docs.xml', 'words.xml').weights()
    assert index_test1 == {1: {'libraries at brown': 0.049999999999999996, 'histori': 0.475, 'univers': 0.475}, 2: {'libraries at brown': 0.475, 'histori': 0.049999999999999996, 'univers': 0.475}, 3: {'libraries at brown': 0.475, 'histori': 0.475, 'univers': 0.049999999999999996}}
    index_test3 = index.Indexer("SearchDesignCheck.xml",'titles.xml', 'docs.xml', 'words.xml').pagerank_prime()
    assert index_test3 == {1: 0.3333333333333333, 2: 0.3333333333333333, 3: 0.3333333333333333}

#this tests edge cases
def test_edge_cases():
    index_test = index.Indexer("PageRankExample5.xml",'titles.xml', 'docs.xml', 'words.xml').trimming()
    assert index_test == {1: {'c'}, 2: set(), 3: {'d'}, 4: {'c'}}
    index_test1 = index.Indexer("PageRankExample5.xml",'titles.xml', 'docs.xml', 'words.xml').weights()
    assert index_test1 == {1: {'a': 0.0375, 'b': 0.0375, 'c': 0.8875, 'd': 0.0375}, 2: {'a': 0.3208333333333333, 'b': 0.0375, 'c': 0.3208333333333333, 'd': 0.3208333333333333}, 3: {'a': 0.0375, 'b': 0.0375, 'c': 0.0375, 'd': 0.8875}, 4: {'a': 0.0375, 'b': 0.0375, 'c': 0.8875, 'd': 0.0375}}
    index_test3 = index.Indexer("PageRankExample5.xml",'titles.xml', 'docs.xml', 'words.xml').pagerank_prime()
    assert index_test3 == {1: 0.04812499999999996, 2: 0.037499999999999964, 3: 0.467938215444088, 4: 0.4464367845559112}



#This tests the id to titles dictionary
def test_correct_dicts():
    index_tester = index.Indexer("PageRankExample1.xml" ,"titles.xml", "docs.xml", "words.xml")
    #Put page rank example 1 as the wiki we look at
    tester_dict = {1: 'a', 2: 'b', 3: 'c'}
    assert index_tester.ids_to_titles == tester_dict

# This tests the titles to id dictionary
def test_correct_dicts2():
    index_tester = index.Indexer('PageRankExample1.xml' ,'titles.xml', 'docs.xml', 'words.xml').titles_to_ids
    assert index_tester == {'a': 1, 'b': 2, 'c': 3}

def test_pagerank_no_links():
    index_test = index.Indexer('PageRankExample1.xml' ,'titles.xml', 'docs.xml', 'words.xml')
    assert index_test.pagerank == {1: 0.43299752423706045, 2: 0.23366914242960607, 3: 0.33333333333333326}

def test_weights():
   index_test = index.Indexer('PageRankExample5.xml' ,'titles.xml', 'docs.xml', 'words.xml') 
   assert index_test.weights == {1: {'a': 0.0375, 'b': 0.0375, 'c': 0.8875, 'd': 0.0375}, 
   2: {'a': 0.3208333333333333, 'b': 0.0375, 'c': 0.3208333333333333, 'd': 0.3208333333333333}, 
   3: {'a': 0.0375, 'b': 0.0375, 'c': 0.0375, 'd': 0.8875}, 4: {'a': 0.0375, 'b': 0.0375, 'c': 0.8875, 'd': 0.0375}}

def test_pagerank_with_links():
    index_test = index.Indexer('PageRankExample5.xml' ,'titles.xml', 'docs.xml', 'words.xml')
    assert index_test.pagerank == {1: 0.04812499999999996, 2: 0.037499999999999964, 3: 0.4686020994775426, 4: 0.4457729005224566}

def test_pagerank_distance():
    index_test = index.Indexer('PageRankExample5.xml' ,'titles.xml', 'docs.xml', 'words.xml')
    assert index_test.distance() == 0.000938873803954454


'''
def test_pagerank_one_word():
    index_test = index.Indexer('PageRankNextExample.xml' ,'titles.xml', 'docs.xml', 'words.xml')
    list_of_values = index_test.pagerank_prime
    assert list_of_values == {1: 0.0481, 2: 0.0375, 3: 0.4686, 4: 0.4458}
'''


def test_seplink_words():
    #basecase
    assert index.Indexer('PageRankExample1.xml' ,'titles.xml', 'docs.xml', 'words.xml').sep_link("[[Heart | Monitor]]") == ('heart', ['Monitor'])
    assert index.Indexer("PageRankExample1.xml" ,"titles.xml", "docs.xml", "words.xml").sep_link("[[Simple | Live]]") == ('simpl', ['Live'])
    #multiple words
    assert index.Indexer("PageRankExample1.xml" ,"titles.xml", "docs.xml", "words.xml").sep_link("[[A lot of words now | what will we do]]") == (('a lot of words now', ['what', 'will', 'we', 'do']))
    #basecase
    assert index.Indexer('PageRankExample1.xml' ,'titles.xml', 'docs.xml', 'words.xml').sep_link("[[Heart | Monitor]]") == ('heart', ['Monitor'])
    assert index.Indexer("PageRankExample1.xml" ,"titles.xml", "docs.xml", "words.xml").sep_link("[[Simple | Live]]") == ('simpl', ['Live'])
    #multiple words
    assert index.Indexer("PageRankExample1.xml" ,"titles.xml", "docs.xml", "words.xml").sep_link("[[A lot of words now | what will we do]]") == (('a lot of words now', ['what', 'will', 'we', 'do']))