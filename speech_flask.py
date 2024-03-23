import os
import pymongo
from flask import Flask, request, jsonify
from pymongo import MongoClient
import speech_recognition as sr
import utils

app = Flask(__name__)

"""
IN THIS CODE I AM TAKING THE AUDIO FILE IN WAV FORMAT FROM ANY LOCATION AND THEN STORING THE GENERATED
TEXT DATA INTO THE MONGODB DATABASE
"""


def mp3_to_text(mp3_file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(mp3_file_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    print("converted the speech data into text!!!")
    return text

def store_text_data(file_name, text_data):

    """
    IN THIS FUNCTION IT EVEN CHECK THAT IF THE TEXT OR THE FILE NAME IS ALREADY PRESENT IN THE DATABASE OR NOT 
    
    """
    client = MongoClient('mongodb://localhost:27017/')
    db = client['mydb']
    collection = db['test']


    if collection.find_one({'$or': [{'file_name': file_name}, {'text': text_data}]}):
        print("File or text data already exists in the database.")
        return  
    
    collection.insert_one({'file_name':file_name, 'text':text_data})
    text_data = utils.text_from_modb()
    sentiments = utils.sentiment_analysis(text_data)
    print("text data stored in mongodb sucessfully!!!")
    return sentiments

    #for text, sentiment in sentiments:
     #print(f"text : {text} and sentiments : {sentiment}")


@app.route('/upload', methods=['post'])
def upload_data():
    if 'file' not in request.files:
        return jsonify({'error':'no file path'})
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error':'No selected files'})
    
    file_path = os.path.join(file.filename)
    file.save(file_path)
    text_data = mp3_to_text(file_path)
    file_name = os.path.basename(file_path)
    sentiments = store_text_data(file_name, text_data)

    if sentiments is not None:
        sentiment_response = [ {'text':text, 'sentiment' : sentiment} for text, sentiment in sentiments]
        return jsonify({'sentiment':sentiment_response})
    else:
        return jsonify({'error':'Failed to retrieve sentiments.'})
    utils.reponse_back_db(sentiment_response)
    return jsonify({'sentiment':sentiment_response})
    


def main():
   app.run(debug=True)
    

if __name__ == '__main__':
    main()