from bottle import route, run, request, get, post
import feedparser
import random
import os
import spacy

@get('/test')
def get_test():
    # Gives the 5 top stories from CNN, BBC, ABC, NYTimes, and Fox News to test article output
    cnnRss = feedparser.parse("http://rss.cnn.com/rss/edition.rss")
    cnnEntries = cnnRss["entries"] # title, summary, link, published
    bbcRss = feedparser.parse("http://feeds.bbci.co.uk/news/rss.xml")
    bbcEntries = bbcRss["entries"] # title, summary, link, published
    abcRss = feedparser.parse("https://www.abc.net.au/news/feed/45910/rss.xml")
    abcEntries = abcRss["entries"] # title, summary, link, published
    nytimesRss = feedparser.parse("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml")
    nytimesEntries = nytimesRss["entries"] # title, summary, link, published
    foxnewsRss = feedparser.parse("http://feeds.foxnews.com/foxnews/latest")
    foxnewsEntries = foxnewsRss["entries"] # title, summary, link, published
    myData = cnnEntries[:1] + bbcEntries[:1] + abcEntries[:1] + nytimesEntries[:1] + foxnewsEntries[:1]
    return {"data":myData}

@get('/random')
def get_random():
    cnnRss = feedparser.parse("http://rss.cnn.com/rss/edition.rss")
    cnnEntries = cnnRss["entries"] # title, summary, link, published
    bbcRss = feedparser.parse("http://feeds.bbci.co.uk/news/rss.xml")
    bbcEntries = bbcRss["entries"] # title, summary, link, published
    abcRss = feedparser.parse("https://www.abc.net.au/news/feed/45910/rss.xml")
    abcEntries = abcRss["entries"] # title, summary, link, published
    nytimesRss = feedparser.parse("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml")
    nytimesEntries = nytimesRss["entries"] # title, summary, link, published
    foxnewsRss = feedparser.parse("http://feeds.foxnews.com/foxnews/latest")
    foxnewsEntries = foxnewsRss["entries"] # title, summary, link, published
    myData = cnnEntries[:5] + bbcEntries[:5] + abcEntries[:5] + nytimesEntries[:5] + foxnewsEntries[:5]
    return {"data":random.choice(myData)}

@get('/sports')
def get_news_article():
    # TODO: Check articles until one passes the test for a certain topic, then return that article
    cnnRss = feedparser.parse("http://rss.cnn.com/rss/edition.rss")
    cnnEntries = cnnRss["entries"] # title, summary, link, published
    bbcRss = feedparser.parse("http://feeds.bbci.co.uk/news/rss.xml")
    bbcEntries = bbcRss["entries"] # title, summary, link, published
    abcRss = feedparser.parse("https://www.abc.net.au/news/feed/45910/rss.xml")
    abcEntries = abcRss["entries"] # title, summary, link, published
    nytimesRss = feedparser.parse("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml")
    nytimesEntries = nytimesRss["entries"] # title, summary, link, published
    foxnewsRss = feedparser.parse("http://feeds.foxnews.com/foxnews/latest")
    foxnewsEntries = foxnewsRss["entries"] # title, summary, link, published
    nlp = spacy.load("training/model-best")
    entries = cnnEntries + bbcEntries + abcEntries + nytimesEntries + foxnewsEntries
    myData = []
    print(len(entries))
    while len(myData) == 0:
        for entry in entries:
            test = nlp(entry['title'])
            if test.cats['RELEVANT'] > 0.95:
                print(test.text)
                print(test.cats['RELEVANT'])
                print(test.cats['IRRELEVANT'])
                myData.append(entry)
                if len(myData) == 5:
                    break
            print(f"The article has a relevant score of {test.cats['RELEVANT']}")
    return {"data":myData}

@get('/training/sports/<title>/<relevant>')
def get_training(title, relevant):
    # TODO: Add article to training data
    relevant = relevant == 'true'
    return {"title":title, "relevant":relevant}

@get('/')
def get_ping():
    return("pong")

if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(host='0.0.0.0', port=8090, debug=True)