import tensorflow as tf
import tensorflow_hub as hub
import pickle
import numpy as np
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def bienvenue():
    return "Bienvenue sur l'API de prédiction de tags pour une question du site StackOverFlow"

@app.route('/predict_tags/<string:question>')
def predict_tags(question):

    # 1. recupération des pickles pour le classifier et le multilabel binarizer
    chemin_mlbinarizer = 'mlbinarizer.pkl'
    with open(chemin_mlbinarizer, 'rb') as file:
        mlbinarizer = pickle.load(file)

    chemin_classifier = 'USEclassifier.pkl'
    with open(chemin_classifier, 'rb') as file:
        USEclassifier = pickle.load(file)

    # 2. transform the question into USE vector
    ## import trained USE model
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
    embedding_model = hub.load(module_url)

    ## define the question as a list 
    print(question)
    question_list=[question]
    
    ## generate embeddings for our question
    embedded_question = embedding_model(question_list)
    print(embedded_question.shape)

    # prédictions
    # Predict on the tag using the best classifier
    tag_pred = USEclassifier.predict(embedded_question)

    # Transform predicted tags back to original format
    prediction = mlbinarizer.inverse_transform(tag_pred)

    data = {'suggested tags for your question' : prediction}

    response=jsonify(data)
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0")
