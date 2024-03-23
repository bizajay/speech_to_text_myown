from pymongo import MongoClient
from textblob import TextBlob

def text_from_modb():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['mydb']
    collection = db['test']
    text_data = [x['text'] for x in collection.find()]
    print("sucessfully taken text data from mongodb!!!!!!!!!")
    return text_data


def sentiment_analysis(text_data):
    sentiments = []
    for text in text_data:
        blob = TextBlob(text)
        sentiment_score = blob.sentiment.polarity
        sentiment = "positive" if sentiment_score > 0 else  "neutral" if sentiment_score == 0 else "negative"
        sentiments.append((text, sentiment))

    return sentiments


def reponse_back_db(setiment_response):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['result']
    collection = db['sentiments']

    collectiom.insert_many(sentiment_response)
    print("sentiment response saved to mongodb!!!!!")








