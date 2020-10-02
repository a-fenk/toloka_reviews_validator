import re

import nltk
from nltk import download
from nltk.corpus import stopwords

from config import Config

download('stopwords', quiet=True)
download('punkt', quiet=True)


def stemmer(corpus):
    stem = nltk.SnowballStemmer("russian").stem
    stems = []
    for word in corpus:
        stems.append(stem(word))
    return stems


def tokenize(corpus):
    # corpus = re.sub(r'\((.*?)\)|[^\w\s]|_', ' ', corpus)  # замена скобок и их содержимое, пунктуации и "_" на " "
    corpus = re.sub(r'[^\w\s]|_', ' ', corpus)  # замена скобок, пунктуации и "_" на " "

    tokens = [word for sent in nltk.sent_tokenize(corpus) for word in nltk.word_tokenize(sent)]
    valuable_words = []

    for token in tokens:
        token = token.lower().strip()
        if token.isalnum() and not token.isdigit():
            valuable_words.append(token)
    return valuable_words


def has_stopword(corpus):
    text = tokenize(corpus)
    stemmed_text = stemmer(text)
    for stopword in Config.STOPWORDS:
        if stopword in text or stopword in stemmed_text:
            return True
    return False


def find_duplicates(str1: str, str2: str):
    list1, list2 = tokenize(str1), tokenize(str2)
    stemmed_list2 = stemmer(list2)
    duplicates = []
    for token in list1:
        if not (token in stopwords.words('russian') or stemmer([token]) in stopwords.words('russian')) and \
                (stemmer([token])[0] in stemmed_list2 or token in stemmed_list2):
            duplicates.append(token)

    return duplicates, True if len(duplicates) == len([token for token in list1 if token not in stopwords.words('russian') and stemmer(token) not in stopwords.words('russian')]) else False


def find_unique(str1: str, str2: str):
    list1, list2 = tokenize(str1), tokenize(str2)
    stemmed_list2 = stemmer(list2)
    unique = []
    for token in list1:
        if not (token in stopwords.words('russian') or stemmer([token]) in stopwords.words('russian')) and \
                (stemmer([token])[0] not in stemmed_list2 and token not in stemmed_list2):
            unique.append(token)

    return unique


def check_for_duplicates(corpus: str):
    tokenized = tokenize(corpus)
    stemmed = stemmer(tokenized)
    duplicates = []
    for index, token in enumerate(tokenized):
        check_list = stemmed.copy()
        del check_list[index]
        if not (token in stopwords.words('russian') or ([token]) in stopwords.words('russian')) and \
                (stemmer([token])[0] in check_list or token in check_list):
            duplicates.append(token)

    return duplicates
