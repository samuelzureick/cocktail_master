import nltk, re, pprint
from nltk import word_tokenize
from urllib import request
from bs4 import BeautifulSoup
import feedparser

llog = feedparser.parse("http://languagelog.ldc.upenn.edu/nll/?feed=atom")
llog['feed']['title']